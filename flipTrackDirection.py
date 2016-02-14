# original by Bernhard Eiser 2014

# 3DE4.script.name:                 ford flip direction
# 3DE4.script.version:              v1.0
# 3DE4.script.gui:                  Manual Tracking Controls::ford
## 3DE4.script.gui.button:  Manual Tracking Controls::Flip Direction, alight-bottom-left , 80 , 20
# 3DE4.script.hide:                 false
# 3DE4.script.startup:              false

def flip_tracking_direction():
    pg              = tde4.getCurrentPGroup()
    cam             = tde4.getCurrentCamera()
    frame           = tde4.getCurrentFrame(cam)
    point_list      = tde4.getPointList(pg, 1)

    if len(point_list) != 1:
        tde4.postQuestionRequester('Point Error', 'Please select exactly one point.', 'OK')
        return

    point_id        = point_list[0]
    current_dir     = tde4.getPointTrackingDirection(pg, point_id)

    if current_dir == 'TRACKING_FW':
        tde4.setPointTrackingDirection(pg, point_id, 'TRACKING_BW')

    elif current_dir == 'TRACKING_BW':
        tde4.setPointTrackingDirection(pg, point_id, 'TRACKING_FW')


flip_tracking_direction()