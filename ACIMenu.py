import acitoolkit.acitoolkit as aci
import sys

def login():
    #get credentials
    creds = aci.Credentials('apic', 'login')
    args = creds.get()
    #login
    session = aci.Session(args.url, args.login, args.password)
    resp = session.login()
    if not resp.ok:
        print('%% Could not login to APIC')
    return args 
    #returns login credentials

def createTenant(username, password, url):
    #login
    session = aci.Session(url, username, password)
    session.login()
    #ask for tenant name and create it
    name = raw_input("Enter tenant name (press 0 to go back): ")
    if name == '0':
        return
    tenant = aci.Tenant(name)
    resp = session.push_to_apic(tenant.get_url(), 
                                tenant.get_json())
    if not resp.ok:
        print('%% Error: Could not push configuration to APIC')
        print(resp.text)
    elif resp.ok:
        print "Tenant \'" + name + "\' created\n"

def getTenants(username,password,url):
    #login
    session = aci.Session(url,username,password)
    session.login()
    #print tenants
    print("TENANT")
    print("------")
    tenants = aci.Tenant.get(session)
    for tenant in tenants:
        print(tenant.name)

def deleteTenant(username, password, url):
    #login
    session = aci.Session(url, username, password)
    session.login()
    #ask for tenant and mark for delete
    name = raw_input("Which tenant would you like to delete? (press 0 to go back) ")
    if name == '0':
        return
    tenant = aci.Tenant(name)
    tenant.mark_as_deleted()
    #make sure user wants to delete before pushing
    x = 0
    while x == 0:
        check = raw_input("Are you sure you want to delete this tenant? (Enter \'yes\' or \'no\') \n")
        #if yes delete tenant
        if check == 'yes': 
            resp = session.push_to_apic(tenant.get_url(), 
                                tenant.get_json())
            if not resp.ok:
                print('%% Error: Could not push configuration to APIC')
                print(resp.text)
            elif resp.ok:
                 print "Tenant \'" + name + "\' deleted\n"
                 break
        #If no then get out of loop         
        elif check == 'no':
            break
        else:
            print "Invalid menu item"

def selectTenant(username, password, url):
    #login
    session = aci.Session(url, username , password)
    session.login()
    #Ask for tenant to select
    x = 0
    while x == 0:
        Name = raw_input("Which tenant do you want to select? (press 0 to go back) ")
        if Name == '0':
            return
        else:    
            tenants = aci.Tenant.get(session)
            str(Name)
            #Check to see if exists and returns it 
            for tenant in tenants:
                if Name == tenant.name:
                    print "Tenant \'" + Name + "\' found"
                    return tenant
            print "Tenant not found"                   

def createVRF(username, password, url, tenant):
    #login
    session = aci.Session(url, username , password)
    session.login()
    #ask for VRF name
    Name = raw_input("Enter VRF name (Press 0 to go back): ")
    if Name == '0':
        return
    #Create VRF
    VRF = aci.Context(Name, tenant)
    resp = session.push_to_apic(tenant.get_url(), tenant.get_json())
    if not resp.ok:
        print('%% Error: Could not push configuration to APIC')
        print(resp.text)
    elif resp.ok:
        print "VRF \'" + Name + "\' Created."
        return VRF

def listVRFs(username, password, url, tenant):
    #login
    session = aci.Session(url, username , password)
    session.login()
    #Get contexts on set tenant
    contexts = aci.Context.get(session, tenant)
    #Print contexts
    for context in contexts:
        print context.name + '\n'

def deleteVRF(username, password, url, tenant):
    #login
    session = aci.Session(url, username, password)
    session.login()
    #ask for tenant and mark for delete
    name = raw_input("Which VRF would you like to delete? (press 0 to go back) ")
    if name == '0':
        return
    else:
        #Get contexts on set tenant
        contexts = aci.Context.get(session, tenant)
        for context in contexts:
            if context.name == name:
                context.mark_as_deleted()
        #make sure user wants to delete before pushing
        x = 0
        while x == 0:
            check = raw_input("Are you sure you want to delete this VRF? (Enter \'yes\' or \'no\') \n")
            #if yes delete tenant
            if check == 'yes': 
                resp = session.push_to_apic(tenant.get_url(), 
                                    tenant.get_json())
                if not resp.ok:
                    print('%% Error: Could not push configuration to APIC')
                    print(resp.text)
                elif resp.ok:
                     print "VRF \'" + name + "\' deleted\n"
                     break
            #If no then get out of loop         
            elif check == 'no':
                break
            else:
                print "Invalid menu item"

def selectVRF(username, password, url, tenant):
    #login
    session = aci.Session(url, username , password)
    session.login()
    #Ask for tenant to select
    name = raw_input("Which VRF would you like to select? (Press 0 to go back) ")
    if name == '0':
        return
    else:
        #Get contexts on set tenant
        contexts = aci.Context.get(session, tenant)
        #Look for tenant
        for context in contexts:
            if context.name == name:
                print "VRF \'" + name + "\' Selected."
                return context
        print "VRF not found"

def createBD(username, password, url, tenant, VRF):
     #login
    session = aci.Session(url, username , password)
    session.login()
    #ask for BD name
    Name = raw_input("Enter BD name (Press 0 to go back):")
    if Name == '0':
            return
    else:
        #Create BD
        BD = aci.BridgeDomain(Name, tenant)
        BD.add_context(VRF)
        resp = session.push_to_apic(tenant.get_url(), tenant.get_json())
        if not resp.ok:
            print('%% Error: Could not push configuration to APIC')
            print(resp.text)
        elif resp.ok:
            print "BD \'" + Name + "\' Created."
            return BD

def deleteBD(username, password, url, tenant, VRF):
     #login
    session = aci.Session(url, username, password)
    session.login()
    #ask for tenant and mark for delete
    name = raw_input("Which BD would you like to delete? (press 0 to go back) ")
    if name == '0':
        return
    else:
        #Get contexts on set tenant
        BDs = aci.BridgeDomain.get(session, tenant)
        for BD in BDs:
            if BD.name == name:
                BD.mark_as_deleted()
        #make sure user wants to delete before pushing
        x = 0
        while x == 0:
            check = raw_input("Are you sure you want to delete this BD? (Enter \'yes\' or \'no\') \n")
            #if yes delete tenant
            if check == 'yes': 
                resp = session.push_to_apic(tenant.get_url(), 
                                    tenant.get_json())
                if not resp.ok:
                    print('%% Error: Could not push configuration to APIC')
                    print(resp.text)
                elif resp.ok:
                     print "BD \'" + name + "\' deleted\n"
                     break
            #If no then get out of loop         
            elif check == 'no':
                break
            else:
                print "Invalid menu item"

def createAP(username, password, url, tenant, bd):
     #login
    session = aci.Session(url, username, password)
    session.login()
    #ask for AP name
    Name = raw_input("Enter AP name (Press 0 to go back):")
    if Name == '0':
            return
    else:
        #Create AP
        AP = aci.AppProfile(Name, tenant)
        AP.attach(bd)
        resp = session.push_to_apic(tenant.get_url(), tenant.get_json())
        if not resp.ok:
            print('%% Error: Could not push configuration to APIC')
            print(resp.text)
        elif resp.ok:
            print "AP \'" + Name + "\' Created."
            return AP

def deleteAP(username, password, url, tenant, bd):
     #login
    session = aci.Session(url, username, password)
    session.login()
    #ask for tenant and mark for delete
    name = raw_input("Which AP would you like to delete? (press 0 to go back) ")
    if name == '0':
        return
    else:
        #Get contexts on set tenant
        APs = aci.APPProfile.get(session, tenant)
        for AP in APs:
            if AP.name == name:
                AP.mark_as_deleted()
        #make sure user wants to delete before pushing
        x = 0
        while x == 0:
            check = raw_input("Are you sure you want to delete this BD? (Enter \'yes\' or \'no\') \n")
            #if yes delete tenant
            if check == 'yes': 
                resp = session.push_to_apic(tenant.get_url(), 
                                    tenant.get_json())
                if not resp.ok:
                    print('%% Error: Could not push configuration to APIC')
                    print(resp.text)
                elif resp.ok:
                     print "BD \'" + name + "\' deleted\n"
                     break
            #If no then get out of loop         
            elif check == 'no':
                break
            else:
                print "Invalid menu item"

def createEPG(username, password, url, tenant, AP, BD):
 #login
    session = aci.Session(url, username, password)
    session.login()
    #Ask for EPG Name
    name = raw_input("Enter EPG Name (Press 0 to go back) : ")
    if name == '0':
            return
    else:
        #Create EPG
        EPG = aci.EPG(name, AP)
        EPG.add_bd(BD)
        resp = session.push_to_apic(tenant.get_url(), tenant.get_json())
        if not resp.ok:
            print('%% Error: Could not push configuration to APIC')
            print(resp.text)
        elif resp.ok:
            print "EPG \'" + name + "\' Created."
            return EPG

def deleteEPG(username, password, url, tenant):
     #login
    session = aci.Session(url, username, password)
    session.login()
    #ask for tenant and mark for delete
    name = raw_input("Which EPG would you like to delete? (press 0 to go back) ")
    if name == '0':
        return
    else:
        #Get EPGS on set tenant
        EPGs = aci.CommonEPG.get(session, tenant)
        for EPG in EPGSs:
            if EPG.name == name:
                EPG.mark_as_deleted()
        #make sure user wants to delete before pushing
        x = 0
        while x == 0:
            check = raw_input("Are you sure you want to delete this EPG? (Enter \'yes\' or \'no\') \n")
            #if yes delete tenant
            if check == 'yes': 
                resp = session.push_to_apic(tenant.get_url(), 
                                    tenant.get_json())
                if not resp.ok:
                    print('%% Error: Could not push configuration to APIC')
                    print(resp.text)
                elif resp.ok:
                     print "EPG \'" + name + "\' deleted\n"
                     break
            #If no then get out of loop         
            elif check == 'no':
                break
            else:
                print "Invalid menu item"

def createInt(username, password, url, tenant, AP, epg):
    # Login to the APIC
    session = aci.Session(url, username, password)
    resp = session.login()
    if not resp.ok:
            print('%% Could not login to APIC')

    #Ask for int info
    print "Enter Physical interface info: \n"
    typ = raw_input("type: ")
    pod = raw_input("pod: ")
    node = raw_input("node: ")
    module = raw_input("module: ")
    port = raw_input("port: ")

    # Create the physical interface object
    intf = aci.Interface(typ, pod, node, module, port)
    #Ask for VLAN info
    print "Enter VLAN interface info: \n"
    name = raw_input("name: ")
    encap_type = raw_input("Encap type: ")
    encap_id = raw_input("Encap ID: ")

    vlan = aci.L2Interface(name, encap_type, encap_id)
    vlan.attach(intf)
    epg.attach(vlan)

    # Push it all to the APIC
    resp = session.push_to_apic(tenant.get_url(), tenant.get_json())
    if not resp.ok:
        print('%% Error: Could not push configuration to APIC')

def createContract(username, password, url, tenant):
    #login
    session = aci.Session(url, username, password)
    session.login()
    #Ask for contract name
    name = raw_input("Enter Contract Name (Press 0 to go back) : ")
    if name == '0':
            return
    else:
        #Create EPG
        cont = aci.Contract(name, tenant)
        esp = session.push_to_apic(tenant.get_url(), tenant.get_json())
        if not esp.ok:
            print('%% Error: Could not push configuration to APIC')
            print(resp.text)
        elif esp.ok:
            print "Contract created"
            return cont
            #print "Creating filter:\n"
        #zxc = 0
        #while zxc == 0:
         #   fname = raw_input("Enter filter name: ")
          #  f = 0
           # applytoFragx = False
            #while f == 0:
             #   ask = raw_input("Does this filter apply to IP fragments? (enter \'yes\' or \'no\')\n")
              #  if ask == 'yes':
               #     applytoFragx = 'yes'
                #    f = 1
                  #  break
                #elif ask == 'no':
                 #   applytoFragx = 'no'
                  #  f = 1
                   # break
                #else:
                 #   print "Invalid input"
            #arpOpcx = ''
            #ask2 = raw_input("Will this filter be applied to ARP requests or replies \n 1) requests \n 2) replies \n 3) unspecified \n")
            #o = 0
            #while o == 0:
             #   if ask2 == '1':
              #      arpOpcx = 'req'
               #     o = 1
                #elif ask2 == '2':
                 #   arpOpcx = 'reply'
                  #  o = 1
                #else:
                 #   print "Invalid input"
            #dFromPortx = raw_input("Enter lowest port number of desitnation port range: ")
            #dToPortx = raw_input("Enter highest port number of destination port range: ")
            #etherTx = 'ip'
            #protx = ''
            #c = 0
            #while c == 0:
             #   ask3 = raw_input("Which L4 protocol whould this filter match? \n 1) TCP \n 2) UDP \n")
              #  if ask3 == '1':
               #     protx = 'tcp'
                #    c = 1
                #elif ask3 == '2':
                 #   protx = 'udp'
                  #  c = 1
                #else:
                 #   print "Invalid input"
            #sFromPortx = raw_input("Enter lowest number of source port range: ")
            #sToPortx = raw_input("Enter highest number of source port range: ")
            #tcpRulesx = 'unspecified'
            #parent = cont
            #entry1 = aci.FilterEntry(fname,
            #            applyToFrag= applytoFragx,
             #           arpOpc= arpOpcx,
              #          dFromPort= dFromPortx,
               #         dToPort= dToPortx,
                #        etherT= 'ip',
                 #       prot= protx,
                  #      sFromPort= sFromPortx,
                   #     sToPort= sToPortx,
                    #    tcpRules= tcpRulesx,
                     #   parent=cont)
            #resp = session.push_to_apic(tenant.get_url(), tenant.get_json())
            #if not resp.ok:
             #   print('%% Error: Could not push configuration to APIC')
              #  print(resp.text)
            #elif resp.ok:
             #   print "Filter \'" + fname + "\' created"
            #v = 0
            #while v == 0:
             #   ask9 = raw_input("Would you like to create another contract? (Enter \'yes\' or \'no\' )")
              #  if ask9 == 'yes':
               #     v= 1
                #elif ask9 == 'no':
                 #   zxc = 1
                  #  v = 1
                #else:
                 #   print "Invalid input"
        #resp = session.push_to_apic(tenant.get_url(), tenant.get_json())
        #if not resp.ok:
         #   print('%% Error: Could not push configuration to APIC')
          #  print(resp.text)
        #elif resp.ok:
         #   print "Contract \'" + cont.name + "\' Created."
          #  return cont


def deleteContract(username, password, url, tenant):
  #login
    session = aci.Session(url, username, password)
    session.login()
    #ask for tenant and mark for delete
    name = raw_input("Which contract would you like to delete? (press 0 to go back) ")
    if name == '0':
        return
    else:
        #Get EPGS on set tenant
        contss = aci.Contract.get(session, tenant)
        for cont in contss:
            if cont.name == name:
                cont.mark_as_deleted()
        #make sure user wants to delete before pushing
        x = 0
        while x == 0:
            check = raw_input("Are you sure you want to delete this contract? (Enter \'yes\' or \'no\') \n")
            #if yes delete tenant
            if check == 'yes': 
                resp = session.push_to_apic(tenant.get_url(), 
                                    tenant.get_json())
                if not resp.ok:
                    print('%% Error: Could not push configuration to APIC')
                    print(resp.text)
                elif resp.ok:
                     print "Contract \'" + name + "\' deleted\n"
                     break
            #If no then get out of loop         
            elif check == 'no':
                break
            else:
                print "Invalid menu item"   

'''def listEPGs(username, password, url, tenant, AP):
    #login
    session = aci.Session(url, username , password)
    session.login()
    #Get contexts on set tenant
    EPGs = aci.CommonEPG.get(session, tenant, )
    #Print contexts
    for EPG in EPGs:
        print EPG.name + '\n

def selectEPG(username, password, url, tenant, AP):
    #login
    session = aci.Session(url, username , password)
    session.login()
    #Ask for tenant to select
    name = raw_input("Which EPG would you like to select? (Press 0 to go back) ")
    if name == '0':
        return
    else:
        #Get contexts on set tenant
        EPGs = aci.Cont.get(session, AP, tenant)
        #Look for tenant
        for EPG in EPGs:
            if EPG.name == name:
                print "EPG \'" + name + "\' Selected."
                return EPG
        print "EPG not found"'''

def addContract(username, password, url, tenant, epg ):
    #login
    session = aci.Session(url, username, password)
    session.login()
    #ask for tenant and mark for delete
    name = raw_input("Which contract would you like to add? (press 0 to go back) ")
    if name == '0':
        return
    else:
        #Get EPGS on set tenant
        contss = aci.Contract.get(session, tenant)
        for cont in contss:
            if cont.name == name:
                r = 0
                while r == 0:
                    det = raw_input("Would you like this epg to consume or provide this contract? \n 1) Consume \n 2) Provide \n")
                    if det == '1':
                        epg.consume(cont)
                        resp = session.push_to_apic(tenant.get_url(), 
                                    tenant.get_json())
                if not resp.ok:
                    print('%% Error: Could not push configuration to APIC')
                    print(resp.text)
                elif resp.ok:
                    print "EPG \'" + epg.name + "\' now consumes contract \'" + cont.name + "\' \n"
                    break

                    if det == '2':
                        epg.provide(cont)
                        resp = session.push_to_apic(tenant.get_url(), 
                                    tenant.get_json())
                        if not resp.ok:
                            print('%% Error: Could not push configuration to APIC')
                            print(resp.text)
                        elif resp.ok:
                            print "EPG \'" + epg.name + "\' now consumes contract \'" + cont.name + "\' \n"
                            break
                        else:
                            print "Invalid menu item"
 




if __name__ == '__main__':
    loginfo = login() #holds onto login credentials
    #Menu options
    x = 0
    while x == 0:
        menu = raw_input("What would you like to do? \n 1) Create tenant \n 2) List tenants\n 3) Delete tenant\n 4) Select tenant\n 5) Exit \n")
        if menu == '1':
            createTenant(loginfo.login, loginfo.password, loginfo.url)
        elif menu == '2':
            getTenants(loginfo.login, loginfo.password, loginfo.url)
        elif menu == '3':
            deleteTenant(loginfo.login, loginfo.password, loginfo.url)
        elif menu == '4':
            tenant = selectTenant(loginfo.login, loginfo.password, loginfo.url) #Hold onto tenant
            if tenant:
                y = 0
                while y == 0:
                    #Seperate menu just for selected tenant
                    menu2 = raw_input("What would you like to do? \n 1) Create VRF \n 2) List VRFs \n 3) Delete VRF \n 4) Select VRF \n 5) Exit \n")
                    if menu2 == '1':
                        createVRF(loginfo.login, loginfo.password, loginfo.url, tenant)
                    elif menu2 == '2':
                        listVRFs(loginfo.login, loginfo.password, loginfo.url, tenant)
                    elif menu2 == '3':
                        deleteVRF(loginfo.login, loginfo.password, loginfo.url, tenant)
                    elif menu2 == '4':
                        VRF = selectVRF(loginfo.login, loginfo.password, loginfo.url, tenant)
                        if VRF:
                            #Seperate menu just for selected VRF
                            j = 0
                            while j == 0:
                                menu3 = raw_input("What would you like to do? \n 1) Create BD \n 2) Delete BD \n 3) Exit \n")
                                if menu3 == '1':
                                    BD = createBD(loginfo.login, loginfo.password, loginfo.url, tenant, VRF)
                                    if BD:
                                        #Seperate menu for BD 
                                        k = 0
                                        while k == 0:
                                            menu4 = raw_input("What would you like to do on BD \'" + BD.name + "\' ? \n 1) Create AP \n 2) Delete AP \n 3) Exit \n")
                                            if menu4 == '1':
                                                AP =createAP(loginfo.login, loginfo.password, loginfo.url, tenant, BD)
                                                if AP:
                                                    #Create menu just for AP
                                                    s = 0
                                                    while s == 0:
                                                        menu5 = raw_input("What would you like to do on AP \'" + AP.name + "\' ? \n 1) Create EPG \n 2) Delete EPG \n 3) Create contract \n 4) Delete contract \n 5) Exit \n")
                                                        if menu5 == '1':
                                                            EPG =createEPG(loginfo.login, loginfo.password, loginfo.url, tenant, AP, BD)
                                                            if EPG:
                                                                a = 0
                                                                while a == 0:
                                                                    menu6 = raw_input("Would you like to attach an interface ? (Type \'yes\' or \'no\') \n")
                                                                    if menu6 == 'yes':
                                                                        createInt(loginfo.login, loginfo.password, loginfo.url, tenant, AP, EPG)
                                                                        #menu for adding contract
                                                                        y = 0
                                                                        while y == 0:
                                                                            menu7 = raw_input("Would you like to add a contract to this epg? (Type \'yes\' or \'no\') \n") 
                                                                            if menu7 == 'yes':
                                                                                cont = addContract(loginfo.login, loginfo.password, loginfo.url, tenant, EPG)
                                                                                print "Contract \'" + cont.name + "\' created"
                                                                                y = 1
                                                                            elif menu7 == 'no':
                                                                                y = 1
                                                                            else:
                                                                                print "Invalid input"
                                                                        a = 1
                                                                    elif menu6 == 'no':
                                                                        #menu for adding contract
                                                                        y = 0
                                                                        while y == 0:
                                                                            menu7 = raw_input("Would you like to add a contract to this epg? (Type \'yes\' or \'no\') \n") 
                                                                            if menu7 == 'yes':
                                                                                addContract(loginfo.login, loginfo.password, loginfo.url, tenant, EPG)
                                                                            elif menu7 == 'no':
                                                                                y = 1
                                                                            else:
                                                                                print "Invalid input"
                                                                        a = 1
                                                                    else:
                                                                        print "Invalid menu item"


                                                        elif menu5 == '2':
                                                            deleteEPG(loginfo.login, loginfo.password, loginfo.url, tenant)
                                                        elif menu5 == '3':
                                                            createContract(loginfo.login, loginfo.password, loginfo.url, tenant)
                                                        elif menu5 == '4':
                                                            deleteContract(loginfo.login, loginfo.password, loginfo.url, tenant)
                                                        elif menu5 == '5':
                                                            #listEPGs(loginfo.login, loginfo.password, loginfo.url, tenant, AP)
                                                            s = 1
                                                        #elif menu5 == '6':
                                                           #EPG = selectEPG(loginfo.login, loginfo.password, loginfo.url, tenant, AP)
                                                           #if EPG:
                                                                #Menu for interface
                                                                #a = 0
                                                               # while a == 0:
                                                                   # menu6 = raw_input("Would you like to attach an interface ? (Type \'yes\' or \'no\') \n")
                                                                  #  if menu6 == 'yes':
                                                                     #   createInt(loginfo.login, loginfo.password, loginfo.url, tenant, AP, EPG)
                                                                     #   a = 1
                                                                     #   menu7 = raw_input("Would you like to add a contract to this epg? (Type \'yes\' or \'no\') \n") 
                                                                   # elif menu6 == 'no':
                                                                     #   a = 1
                                                                    #else:
                                                                       # print "Invalid menu item"
                                                        #elif menu5 == '7':
                                                           # s = 1
                                                        else:
                                                            print "Invalid menu item"
                                            elif menu4 == '2':
                                                deleteAP(loginfo.login, loginfo.password, loginfo.url, tenant, BD)
                                            elif menu4 == '3':
                                                k = 1
                                            else:
                                                print "Invalid menu item"
                                elif menu3 == '2':
                                    deleteBD(loginfo.login, loginfo.password, loginfo.url, tenant, VRF)
                                elif menu3 == '3':
                                    j = 1
                                else:
                                    print "Invalid menu item"
                    elif menu2 == '5':
                        y = 1
                    else:
                        print "Invalid menu item"
        elif menu == '5':
            sys.exit()
        else:
            print "invalid menu item"


    