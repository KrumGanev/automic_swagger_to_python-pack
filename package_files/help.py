class help():
    def __init__(self, module=None, html=False): 
        if module == None:
            if html:
                self.show_all_html()
            else:
                self.show_all()
        else:
            self.show_module(module)

    def show_module(self, module): 
        for parent in help_list: 
            for child in help_list[parent]:
                if child == module:
                    print("\n- " + child +"\n")
                    print("    parent  - " + parent )
                    print("    summary - " + help_list[parent][child]['summary'] )
                    print("    path    - " + help_list[parent][child]['path'] )
                    print("    method  - " + help_list[parent][child]['method'] )
                    print("")
    
    def show_all(self): 
        for parent in help_list: 
            for f in help_list[parent]: 
                print(" - " + f )
                print("     - parent  - " + parent )
                print("     - summary - " + help_list[parent][f]['summary'] )
                print("     - path    - " + help_list[parent][f]['path'] )
                print("     - method  - " + help_list[parent][f]['method'] )
                print("")
    
    def show_all_html(self): 
        import json
        
        print('## automic_rest (python client)')
        print('![version](https://img.shields.io/badge/version-0.0.5-blue) ![coverage](https://img.shields.io/badge/coverage-80%25-yellowgreen) ![state](https://img.shields.io/badge/state-dev-red) ![automic](https://img.shields.io/badge/automic-12.3-green)')
        print('#')
        print('Automic-Rest-Client generated from AE/Swagger <br>')
        print('<a >https://docs.automic.com/documentation/webhelp/english/all/components/DOCU/21/REST%20API/Automation.Engine/swagger.json</a>')
        print('#')
        
        print("<ul>")
        for module in help_list: 
            print('     <li>')
            print('         <a href="#'+module+'">'+module+'</a>')
            print('         <ul>')
            for f in help_list[module]: 
                print('             <li><a href="#'+f+'">'+f+'</a></li>')
            print("         </ul>")
            print("     </li>")
        print("</ul>")

        for module in help_list: 
            print('     <div id="'+module+'">')
            print('     <h3>'+module+'</h3>')
            for f in help_list[module]:    
                print('         <div id="'+f+'">')
                print('         <h4>'+f+'</h4>')
                print("             <ul>")
                print("                 <li>summary - " + help_list[module][f]['summary'] + "</li>")
                print("                 <li>path - " + help_list[module][f]['path'] + "</li>")
                print("                 <li>method - " + help_list[module][f]['method'] + "</li>")
                print("             </ul>")
                print("             <div>Parameters: </div>")
                print("             <div><pre>" + json.dumps(help_list[module][f]['parameters'], indent=4, sort_keys=True) + "</pre></div>")
                print("             <div>Code-Example: </div>")
                print('             <pre>CODE</pre>')
                print('         </div>')
            print("         </ul>")
            print("     </div>")
        
        #print("<table>")
        #print("<thead><th>Class</th><th>Function</th><th>Infos</th><th>Parameters</th></thead>")
        #print("<tbody>")
        #for module in help_list: 
        #    for f in help_list[module]: 
        #        print("     <tr><td>"+module+"</td>")
        #        print("     <td>"+f+"</td>")
        #        print("     <td>")
        #        print("         <ul>")
        #        print("             <li>summary - " + help_list[module][f]['summary'] + "</li>")
        #        print("             <li>path - " + help_list[module][f]['path'] + "</li>")
        #        print("             <li>method - " + help_list[module][f]['method'] + "</li>")
        #        print("         </ul>")
        #        print("     </td>")
        #        print("     <td><pre>" + json.dumps(help_list[module][f]['parameters'], indent=4, sort_keys=True) + "</pre></td>")
        #        print("     </tr>")
        #        
        #print("</tbody>")
        #print("</table>")

