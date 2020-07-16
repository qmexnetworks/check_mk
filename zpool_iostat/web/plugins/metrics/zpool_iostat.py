#!/usr/bin/env python

metric_info["zpool_iostat_read_ops"] = {
    'title': _('zpool read operations'),
    "unit": "1/s",
    "color": "#000000",
}

metric_info["zpool_iostat_write_ops"] = {
    'title': _('zpool write operations'),
    "unit": "1/s",
    "color": "#00bb33",
}

metric_info["zpool_iostat_write_tps"] = {
    'title': _('zpool write throughput'),
    "unit": "B/s",
    "color": "#e70000",
}

metric_info["zpool_iostat_read_tps"] = {
    'title': _('zpool read throughput'),
    "unit": "B/s",
    "color": "#00bb33",
}

graph_info.["zpool_iostat"]{
    'title': _('zpool iops'),
    'metrics': [ ( 'zpool_iostat_read_ops', 'line' ),
                 ( 'zpool_iostat_write_ops', 'line' ),
               ],
    }