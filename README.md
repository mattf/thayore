Display map with: gvmap.sh -Ae -Tpng layout.dot | display -

Simulate a single process: python process.py <model.dot>

Dependencies:
 * qpid-proton
 * pydot
 * null

## TODO
 * model preso, top of hour signals beginning, 45 min signals end
 * gravity to remain during preso
 * handle distance, maybe as min duration in a node, e.g. can't move from room to hallway to new room in .5s
 * dropped samples, e.g. missed enter or leave
 * if preo left between begin & end, should not return until next begin
 * model distance from locations
