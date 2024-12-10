from graph import Node, NodeVisitLogger, searchBreathFirst

root = Node("root", 0)
child1 = Node("child1", 1)
child2 = Node("child2", 2)
child3 = Node("child3", 3)

root.addChild(child1)
root.addChild(child2)
child2.addChild(child3)

with NodeVisitLogger() as logger:
    print(searchBreathFirst(root, content=3).id)
    print(logger.get())
