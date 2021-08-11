class help():
    def __init__(self, module=None): 
        if module == None:
            self.show_all()
        else:
            self.show_module(module)

    def show_module(self, module): 
        print(module)
        for f in help_list[module]: 
            print("   - " + f )
            print("       summary - " + help_list[module][f]['summary'] )
            print("       path - " + help_list[module][f]['path'] )
            print("       method - " + help_list[module][f]['method'] )
            print("")
    
    def show_all(self): 
        for module in help_list: 
            print("*    "+module)
            for f in help_list[module]: 
                print("     *   " + f )
                print("         *   summary - " + help_list[module][f]['summary'] )
                print("         *   path - " + help_list[module][f]['path'] )
                print("         *   method - " + help_list[module][f]['method'] )
                print("")
    
    def show_all_html(self): 
        import json
        print("<table>")
        print("<thead><th>Class</th><th>Function</th><th>Infos</th><th>Parameters</th></thead>")
        print("<tbody>")
        for module in help_list: 
            for f in help_list[module]: 
                print("     <tr><td>"+module+"</td>")
                print("     <td>"+f+"</td>")
                print("     <td>")
                print("         <ul>")
                print("             <li>summary - " + help_list[module][f]['summary'] + "</li>")
                print("             <li>path - " + help_list[module][f]['path'] + "</li>")
                print("             <li>method - " + help_list[module][f]['method'] + "</li>")
                print("         </ul>")
                print("     </td>")
                print("     <td><pre>" + json.dumps(help_list[module][f]['parameters'], indent=4, sort_keys=True) + "</pre></td>")
                print("     </tr>")
                
        print("</tbody>")
        print("</table>")


