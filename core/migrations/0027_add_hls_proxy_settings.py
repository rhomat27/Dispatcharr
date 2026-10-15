"""Add native-HLS controls without changing existing proxy behavior."""

from django.db import migrations


HLS_PROXY_DEFAULTS = {
    "hls_segment_duration_seconds": 4,
    "hls_window_size": 10,
    "hls_initial_playlist_seconds": 4,
    "hls_live_edge_holdback_seconds": 0,
}


def add_hls_proxy_settings(apps, schema_editor):
    CoreSettings = apps.get_model("core", "CoreSettings")
    try:
        settings = CoreSettings.objects.get(key="proxy_settings")
    except CoreSettings.DoesNotExist:
        return

    value = settings.value if isinstance(settings.value, dict) else {}
    updated = {**HLS_PROXY_DEFAULTS, **value}
    if updated != value:
        settings.value = updated
        settings.save(update_fields=["value"])


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0026_add_channel_client_wait_period"),
    ]

    operations = [
        migrations.RunPython(add_hls_proxy_settings, migrations.RunPython.noop),
    ]
