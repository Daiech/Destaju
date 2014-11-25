def is_repeated_tool(formset):
    tool_list = []
    repeated_tool = False
    for q_form in formset.forms:
        tool_form = q_form.cleaned_data.get('tool')
        if tool_form:
            if tool_form.id in tool_list:
                repeated_tool = True
                break
            tool_list.append(tool_form.id)
    return repeated_tool