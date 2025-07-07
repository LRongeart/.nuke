# TRACTOR BLADE MATCHING TROUBLESHOOTING GUIDE
# 
# If jobs are being submitted but not picked up by blades, try these steps:
#
# 1. Use the "Debug: Show Available Blades" button to see what services/envkeys 
#    the blades are advertising
#
# 2. Compare the job's service/envkey with what the blades expect
#
# 3. Common service names to try:
#    - NukeRender, NukeXRender
#    - nuke, nukex
#    - render
#
# 4. Common envkey formats to try:
#    - nuke-15.1, nukex-15.1
#    - nuke15.1, nukex15.1  
#    - nuke, nukex
#    - (leave blank to match any)
#
# 5. Check blade crews - make sure they include "3D4" or try removing crews entirely
#
# 6. Try changing tier from "windows" to "linux" or remove it entirely
#
# 7. Run the test_blade_matching.py script to systematically test combinations
#
# 8. In Tractor UI, check the "Why Blocked?" feature for the job
#
# 9. Check blade logs for matching errors
#
# 10. Common fixes:
#     - Remove tier restriction
#     - Use simpler service names like "render" 
#     - Leave envkey blank to match any environment
#     - Remove or modify crews requirement
