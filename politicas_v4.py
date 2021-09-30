
#################################################################################################################################################
# politicas_v3.py
#
# @autores: Luisa Quiroga y Junior Palomino
#
# Programa que permite listar las politicas de backups (programadas) que tienen asignados los boot volumes y block volumes de un tenancy completo
# El programa hace el recorrido por todos compartimientos y dominios de disponibilidad especificos de una region 
#################################################################################################################################################

import oci
import sys

#primero se deben obtener todos los compartments del tenant, listarlos, y entrar al loop de core_client.list_boot_volumes() y core_client.list_volumes()

#funcion predefinida de obtener todos los compartments
def identity_read_compartments(identity, tenancy):

    global cmd
    print("Loading Compartments...")
    try:
        compartments = oci.pagination.list_call_get_all_results(
            identity.list_compartments,
            tenancy.id,
            compartment_id_in_subtree=True,
        ).data

        # Add root compartment which is not part of the list_compartments
        compartments.append(tenancy)

        # compile new compartment object
        filtered_compartment = []
        for compartment in compartments:
            # skip non active compartments
            if compartment.id != tenancy.id and compartment.lifecycle_state != oci.identity.models.Compartment.LIFECYCLE_STATE_ACTIVE:
                continue

            filtered_compartment.append(compartment)

        print("    Total " + str(len(filtered_compartment)) + " compartments loaded.")
        return filtered_compartment

    except Exception as e:
        raise RuntimeError("Error in identity_read_compartments: " + str(e.args))


def main():
    arg = "all"
    if len(sys.argv) > 1:
    	arg = sys.argv[1]
    if arg == "all":
        print("Lista todos los Boot Volume y Block Volume en el tenant y sus politicas de backup")
    elif arg == "conbackup":
        print("Lista los Boot Volume y Block Volume que tienen politicas de backup en el tenant")
    elif arg == "sinbackup":
        print("Lista los Boot Volume y Block Volume que NO tienen politicas de backup")
	# Create a default config using DEFAULT profile in default location
    config = oci.config.from_file()
	
    # Initialize service client with default config file
    core_client = oci.core.BlockstorageClient(config)

    # Identity extract compartments
    # config, signer = create_signer(config, cmd.is_instance_principals, cmd.is_delegation_token)
    compartments = []
    tenancy = None

    identity = oci.identity.IdentityClient(config)

    tenancy = identity.get_tenancy(config["tenancy"]).data
    print("tenancy_ocid: " + tenancy.id)

    compartments = identity_read_compartments(identity, tenancy)

    for compartment in compartments:
       
        
        #listar boot volumes para un compartment especifico
        list_availability_domains_response = identity.list_availability_domains(compartment_id=compartment.id)
        for availability_domain_aux in list_availability_domains_response.data:
            list_boot_volumes_response = core_client.list_boot_volumes(availability_domain=availability_domain_aux.name, compartment_id=compartment.id)
            
            #listar todos los boot volume de un AD especifico
            j=1
            for boot_volume in list_boot_volumes_response.data:
                
                #consuslta las politicas por volumen
                politicas = core_client.get_volume_backup_policy_asset_assignment(boot_volume.id)
                
                if (arg == "conbackup" and len(politicas.data) > 0) or arg == "all":
                    print("******************************Boot Volume "+str(j)+ availability_domain_aux.name + " Compartment: " + compartment.name +"*****************************") 
                    print("OCID del boot volume: "+boot_volume.id)
                    print("Nombre del boot volume: "+boot_volume.display_name)
                    #consulta el detalle de la politica por cada politica (solo puede haber una)
                    for politica in politicas.data:
                        pol = core_client.get_volume_backup_policy(politica.policy_id)
                        print("Tipo de politica: "+pol.data.display_name)
                        print(pol.data.schedules)
                    print("___________________________")
                    print()
                    print()
                    j = j+1
                elif arg == "sinbackup" and len(politicas.data) < 1 or arg == "all":
                    print("******************************Boot Volume "+str(j)+ availability_domain_aux.name + " Compartment: " + compartment.name +"*****************************") 
                    print("OCID del boot volume: "+boot_volume.id)
                    print("Nombre del boot volume: "+boot_volume.display_name)
                    print("___________________________")
                    print()
                    print()
                    j = j+1
                    
                    
        #listar boot volumes para un compartment especifico
        
        list_volumes_response = core_client.list_volumes(compartment_id=compartment.id)
        i=1
        for volume in list_volumes_response.data:
            
            #consuslta las politicas por volumen
            politicas = core_client.get_volume_backup_policy_asset_assignment(volume.id)
            if (arg == "conbackup" and len(politicas.data) > 0) or arg == "all":
                print("******************************Block Volume "+str(i)+ " Compartment: " + compartment.name +"*****************************") 
                print("OCID del volume: "+volume.id)
                print("Nombre del volume: "+volume.display_name)
                #print(politicas.data)
                #consulta el detalle de la politica por cada politica (solo puede haber una)
                for politica in politicas.data:
                    pol = core_client.get_volume_backup_policy(politica.policy_id)
                    print("Tipo de politica: "+pol.data.display_name)
                    print(pol.data.schedules)
                print("___________________________")
                print()
                print()
                i = i+1
            elif arg == "sinbackup" and len(politicas.data) < 1 or arg == "all":
                print("******************************Block Volume "+str(i)+ " Compartment: " + compartment.name +"*****************************") 
                print("OCID del volume: "+volume.id)
                print("Nombre del volume: "+volume.display_name)
                print("___________________________")
                print()
                print()
                i = i+1
            
        


main()
