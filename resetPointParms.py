# 3DE4.script.name:                 ford reset point
# 3DE4.script.version:              v1.0
# 3DE4.script.comment:              sets manual point defaults
# 3DE4.script.gui:                  Manual Tracking Controls::ford
## 3DE4.script.gui.button:           Manual Tracking Controls::reset point, alight-bottom-left , 80 , 20
# 3DE4.script.hide:                 false
# 3DE4.script.startup:              false

def reset_point_parameters():
    group_id    = tde4.getCurrentPGroup()
    cam         = tde4.getCurrentCamera()
    frame       = tde4.getCurrentFrame(cam)
    point_list  = tde4.getPointList(group_id, 1)

    if len(point_list) != 1:
        tde4.postQuestionRequester("Point Error", "Please select exactly one point.", "OK")
        return

    point_id    = point_list[0]

    tde4.setPointTrackingMode(group_id, point_id, 'TRACKING_PATTERN')
    tde4.setPointRGBWeights(group_id, point_id, 0.5, 1, 0)
    tde4.setPointBlurring(group_id, point_id, 'BLUR_NONE')
    tde4.setPointEnhancedTrackingFlag(group_id, point_id, 1)
    tde4.setPointLuminanceChangesFlag(group_id, point_id, 0)
    tde4.setPointRotatePatternFlag(group_id, point_id, 0)
    tde4.setPointScalePatternFlag(group_id, point_id, 0)



reset_point_parameters()