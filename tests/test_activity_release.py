"""Library-only release packaging and integrity regressions; no SDK/network."""
import importlib.util
import io,tarfile,sys
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import test_github_release as generic


REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(REPO/"scripts"))
from repo_workflow import record_build
spec = importlib.util.spec_from_file_location("package_release", REPO / "scripts/package-release.py")
packager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packager)


class LibraryPackagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "package.json").write_text(json.dumps({"name": "fixture", "version": "1.2.3"}))

    def candidate(self):
        folder=self.root/'build/candidate';folder.mkdir(parents=True,exist_ok=True)
        sdk=folder/'dist.zip';sdk.write_bytes(generic.zip_bytes({'js/index.js':b'SDK'}))
        files={'package.json':(self.root/'package.json').read_bytes(),'dist.zip':sdk.read_bytes()}
        candidate=folder/'fixture-1.2.3.tgz'
        with tarfile.open(candidate,'w:gz') as archive:
            for name,data in files.items():
                member=tarfile.TarInfo('package/'+name);member.size=len(data);archive.addfile(member,io.BytesIO(data))
        record_build(self.root,sdk)
        return sdk,candidate

    def test_packages_without_any_timer_checkout_or_pbw(self):
        (self.root/'dist.zip').write_bytes(b'historical root SDK')
        sdk,candidate=self.candidate()
        with patch('subprocess.run',side_effect=AssertionError('Freezing must not rebuild')):
            packager.package(self.root,sdk)
        self.assertEqual({p.name for p in (self.root/'releases').iterdir()},
            {'fixture-1.2.3.tgz','fixture-1.2.3-sdk.zip','SHA256SUMS-1.2.3.txt'})
        paths=['releases/fixture-1.2.3-sdk.zip','releases/fixture-1.2.3.tgz']
        sums=(self.root/'releases/SHA256SUMS-1.2.3.txt').read_bytes()
        hashes=generic.release.checksum_map(sums,paths,'releases/SHA256SUMS-1.2.3.txt')
        for name in paths:self.assertEqual(hashes[name],generic.release.digest((self.root/name).read_bytes()))
        self.assertEqual((self.root/'releases/fixture-1.2.3.tgz').read_bytes(),candidate.read_bytes())
        self.assertEqual((self.root/'dist.zip').read_bytes(),b'historical root SDK')

    def test_packaging_preserves_historical_timer_and_library_artifacts(self):
        old={'Activity-Timer-0.1.0.pbw':b'old timer','pebble-activities-0.1.0.tgz':b'old package','SHA256SUMS.txt':b'old checksums'}
        releases=self.root/'releases';releases.mkdir()
        for name,data in old.items():(releases/name).write_bytes(data)
        sdk,_=self.candidate();packager.package(self.root,sdk)
        for name,data in old.items():self.assertEqual((releases/name).read_bytes(),data)
        self.assertNotIn('.pbw',(releases/'SHA256SUMS-1.2.3.txt').read_text())

    def test_unbuilt_or_corrupt_sdk_does_not_touch_release_files(self):
        releases=self.root/'releases';releases.mkdir();sums=releases/'SHA256SUMS.txt';sums.write_bytes(b'unchanged')
        with self.assertRaises((ValueError,FileNotFoundError)):packager.package(self.root)
        sdk,_=self.candidate();sdk.write_bytes(b'corrupt SDK');record_build(self.root,sdk)
        with self.assertRaises(zipfile.BadZipFile):packager.package(self.root,sdk)
        self.assertEqual(list(releases.iterdir()),[sums]);self.assertEqual(sums.read_bytes(),b'unchanged')


class LibraryReleaseTests(unittest.TestCase):
    setUp = generic.ReleaseTests.setUp
    tearDown = generic.ReleaseTests.tearDown
    run_git = generic.ReleaseTests.run_git
    write = generic.ReleaseTests.write
    commit = generic.ReleaseTests.commit

    def test_activities_release_accepts_only_library_artifacts(self):
        assets = {name: (self.root / name).read_bytes()
                  for name in ["dist.zip", "releases/fixture-1.2.3.tgz"]}
        config = {**self.config, "kind": "activities"}
        generic.release.validate_artifacts(self.root, config, self.original, self.package, assets)
        with self.assertRaisesRegex(ValueError, "only the library"):
            generic.release.validate_artifacts(self.root, config, self.original, self.package,
                {**assets, "releases/Activity-Timer-1.2.3.pbw": b"unrelated app"})


if __name__ == "__main__":
    unittest.main()
