from taxi_pipeline.manifest import Manifest, ManifestEntry


def test_manifest_marks_month_complete(tmp_path):
    path = tmp_path / "manifest.json"
    manifest = Manifest(path)
    assert not manifest.is_complete("yellow", 2025, 1)

    manifest.upsert(ManifestEntry("yellow", 2025, 1, "x.parquet", "complete", 100))
    reloaded = Manifest(path)

    assert reloaded.is_complete("yellow", 2025, 1)
