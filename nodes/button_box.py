import CostumePy


def get_state():
    return {"b1": True, "b2": False, "k1": 10, "k2": 0}


node = CostumePy.new_node("button_box")

state = {"b1": False, "b2": False, "k1": 0, "k2": 0}

for item in state:
    if item[0] == "b":
        node.ui.add_button(item, item)
        node.ui.get(item)["enabled"] = False

node.ui.update()

while node.running:

    state_changes = {}
    new_state = get_state()
    for item in new_state:
        if new_state[item] != state[item]:
            state_changes[item] = new_state[item]
            node.ui.get(item)["button_class"] = "btn btn-default" if new_state[item] else "btn btn-success"

    if state_changes:
        node.broadcast("button_input", state_changes)
        node.ui.update()

    state = new_state