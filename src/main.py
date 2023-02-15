import os
import random
import telebot
import requests
import json
from optparse import OptionParser
from telebot import types

import integrateYC

parser = OptionParser()
parser.add_option(
    "-d", "--dev", dest="dev_mod", help="Use DEV Telegram Bot", default=False
)
(option, args) = parser.parse_args()

if option.dev_mod:
    bot_token = os.environ.get("BOT_TOKEN_LOCAL")
    iam_access_token = integrateYC.get_iam_local()
else:
    bot_token = os.environ.get("BOT_TOKEN_PROD")
    iam_access_token = integrateYC.get_iam_serverless()


bot = telebot.TeleBot(bot_token)


# --------------------- bot ---------------------
@bot.message_handler(commands=["help"])
def say_welcome(message):
    bot.send_message(
        message.chat.id,
        "Привет, я помогу тебе управлять инфраструктурой в YC\n"
        "Исходники здесь [here](https://github.com/try-cat-ch/telegram-cloud-manager",
        parse_mode="markdown",
    )


@bot.message_handler(commands=['start'])
def start_message(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    list_organizations_button = types.KeyboardButton("List organizations")
    list_clouds_button = types.KeyboardButton("List clouds")
    list_folders_button = types.KeyboardButton("List folders")
    list_vms_button = types.KeyboardButton("List VMs")
    init_create_button = types.KeyboardButton("Create")
    start_vm_button = types.KeyboardButton("Start")
    stop_vm_button = types.KeyboardButton("Stop")
    restart_vm_button = types.KeyboardButton("Restart")
    delete_button = types.KeyboardButton("Delete")

    markup.add(init_create_button)
    markup.add(start_vm_button)
    markup.add(stop_vm_button)
    markup.add(restart_vm_button)
    markup.add(delete_button)
    markup.add(list_vms_button)
    markup.add(list_folders_button)
    markup.add(list_clouds_button)
    markup.add(list_organizations_button)
    
    bot.send_message(message.chat.id, "Select",  reply_markup=markup)


@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == "List organizations":
        organizations_info = integrateYC.get_organizations(iam_access_token)

        bot.send_message(message.chat.id, str(organizations_info))
        start_message(message)

    elif message.text == "List clouds":
        markup = types.InlineKeyboardMarkup()
        list_organizations = integrateYC.get_organizations(iam_access_token)
        for organization in list_organizations.get("organizations"):
            markup.add(types.InlineKeyboardButton(text=str(organization.get("name")), callback_data=str("list-clouds-set-organization-" + organization.get("id"))))

        return_button = types.InlineKeyboardButton("Return", callback_data="return")
        markup.add(return_button)

        bot.send_message(message.chat.id, "Set organization", reply_markup=markup)

    elif message.text == "List folders":
        markup = types.InlineKeyboardMarkup()
        list_organizations = integrateYC.get_organizations(iam_access_token)
        for organization in list_organizations.get("organizations"):
            markup.add(types.InlineKeyboardButton(text=str(organization.get("name")), callback_data=str("list-folders-set-organization-" + organization.get("id"))))

        return_button = types.InlineKeyboardButton("Return", callback_data="return")
        markup.add(return_button)

        bot.send_message(message.chat.id, "Set organization", reply_markup=markup)
        
    elif message.text=="List VMs":
        markup = types.InlineKeyboardMarkup()
        list_organizations = integrateYC.get_organizations(iam_access_token)
        for organization in list_organizations.get("organizations"):
            markup.add(types.InlineKeyboardButton(text=str(organization.get("name")), callback_data=str("list-vms-set-organization-" + organization.get("id"))))

        return_button = types.InlineKeyboardButton("Return", callback_data="return")
        markup.add(return_button)

        bot.send_message(message.chat.id, "Set organization", reply_markup=markup)		

    elif message.text=="Create":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

        create_instance_button = types.KeyboardButton("Create instance")
        create_vpc_button = types.KeyboardButton("Delete VPC[not ready]")
        return_button = types.KeyboardButton("Return")

        markup.add(create_instance_button)
        markup.add(create_vpc_button)
        markup.add(return_button)
        
        bot.send_message(message.chat.id, "What you want create?", reply_markup=markup)	
        return
    
    elif message.text == "Create instance":
        markup = types.InlineKeyboardMarkup()
        list_organizations = integrateYC.get_organizations(iam_access_token)
        for organization in list_organizations.get("organizations"):
            markup.add(types.InlineKeyboardButton(text=str(organization.get("name")), callback_data=str("create-vm-set-organization-" + organization.get("id"))))

        return_button = types.InlineKeyboardButton("Return", callback_data="return")
        markup.add(return_button)

        bot.send_message(message.chat.id, "Set organization", reply_markup=markup)	

    elif message.text == "Delete":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

        delete_instance_button = types.KeyboardButton("Delete instance")
        delete_vpc_button = types.KeyboardButton("Delete VPC[not ready]")
        return_button = types.KeyboardButton("Return")

        markup.add(delete_instance_button)
        markup.add(delete_vpc_button)
        markup.add(return_button)
        

        bot.send_message(message.chat.id, "What you want delete?", reply_markup=markup)	
        #return

    elif message.text == "Delete instance":
        markup = types.InlineKeyboardMarkup()
        list_organizations = integrateYC.get_organizations(iam_access_token)
        for organization in list_organizations.get("organizations"):
            markup.add(types.InlineKeyboardButton(text=str(organization.get("name")), callback_data=str("delete-vm-set-organization-" + organization.get("id"))))

        return_button = types.InlineKeyboardButton("Return", callback_data="return")
        markup.add(return_button)

        bot.send_message(message.chat.id, "Set organization", reply_markup=markup)


    # Start
    elif message.text == "Start":
        markup = types.InlineKeyboardMarkup()
        list_organizations = integrateYC.get_organizations(iam_access_token)
        for organization in list_organizations.get("organizations"):
            markup.add(types.InlineKeyboardButton(text=str(organization.get("name")), callback_data=str("start-vm-set-organization-" + organization.get("id"))))

        return_button = types.InlineKeyboardButton("Return", callback_data="return")
        markup.add(return_button)

        bot.send_message(message.chat.id, "Set organization", reply_markup=markup)
    
    # Stop
    elif message.text == "Stop":
        markup = types.InlineKeyboardMarkup()
        list_organizations = integrateYC.get_organizations(iam_access_token)
        for organization in list_organizations.get("organizations"):
            markup.add(types.InlineKeyboardButton(text=str(organization.get("name")), callback_data=str("stop-vm-set-organization-" + organization.get("id"))))

        return_button = types.InlineKeyboardButton("Return", callback_data="return")
        markup.add(return_button)

        bot.send_message(message.chat.id, "Set organization", reply_markup=markup)


    # Restart
    elif message.text == "Restart":
        markup = types.InlineKeyboardMarkup()
        list_organizations = integrateYC.get_organizations(iam_access_token)
        for organization in list_organizations.get("organizations"):
            markup.add(types.InlineKeyboardButton(text=str(organization.get("name")), callback_data=str("restart-vm-set-organization-" + organization.get("id"))))

        return_button = types.InlineKeyboardButton("Return", callback_data="return")
        markup.add(return_button)

        bot.send_message(message.chat.id, "Set organization", reply_markup=markup)  

    # Return
    elif message.text == "Return":
        start_message(message)

@bot.callback_query_handler(func=lambda call: call.data.startswith("return"))
def return_to_start_menu(callback):
    start_message(callback.message)


@bot.callback_query_handler(func=lambda call: call.data.startswith("create-vm"))
def create_vm(callback):
    if "create-vm-folder-image-" in callback.data:
        # TODO: add subnet in parameters
        create_vm_info = integrateYC.create_vm(access_token=iam_access_token, 
                                                folder_id=str(callback.data).split("-")[-2], 
                                                image_id=str(callback.data).split("-")[-1])

        bot.send_message(callback.message.chat.id, str(create_vm_info))
        start_message(callback.message)
    elif "create-vm-set-org-set-cld-set-fldr-" in callback.data:
        markup = types.InlineKeyboardMarkup()

        folder_id = str(callback.data).split("-")[-1]
        images = [("Ubuntu 22.04", "fd8emvfmfoaordspe1jr"), ("custom", "fd8n8r3ab6dsvqbebcij")]

        for image in images:
            markup.add(types.InlineKeyboardButton(text=image[0], callback_data="create-vm-folder-image-" + folder_id + "-" + image[1]))

        return_button = types.InlineKeyboardButton("Return", callback_data="return")
        markup.add(return_button)

        bot.send_message(callback.message.chat.id, "Set folder", reply_markup=markup)

    elif "create-vm-set-organization-set-cloud-" in callback.data:
        folders_info = integrateYC.get_folders(access_token=iam_access_token, cloud=str(callback.data).split("-")[-1])
        markup = types.InlineKeyboardMarkup()
        for folder in folders_info.get("folders"):
            button_name = str(folder.get("name"))
            button_callback = str("create-vm-set-org-set-cld-set-fldr-" + folder.get("id"))
            markup.add(types.InlineKeyboardButton(text=button_name, callback_data=button_callback))
            
        return_button = types.InlineKeyboardButton("Return", callback_data="return")
        markup.add(return_button)

        bot.send_message(callback.message.chat.id, "Set folder", reply_markup=markup) 
    elif "create-vm-set-organization" in callback.data:
        markup = types.InlineKeyboardMarkup()
        clouds_info = integrateYC.get_clouds(access_token=iam_access_token, organization=str(callback.data).split("-")[-1])
        for cloud in clouds_info.get("clouds"):
            markup.add(types.InlineKeyboardButton(text=str(cloud.get("name")), callback_data=str("create-vm-set-organization-set-cloud-" + cloud.get("id"))))

        return_button = types.InlineKeyboardButton("Return", callback_data="return")
        markup.add(return_button)

        bot.send_message(callback.message.chat.id, "Set cloud", reply_markup=markup) 


@bot.callback_query_handler(func=lambda call: call.data.startswith("delete-vm"))
def delete_vm(callback):
    # Delete
    if "delete-vm-folder-id-" in callback.data:
        delete_vm_info = integrateYC.delete_vm(iam_access_token, str(callback.data).split("-")[-1])

        bot.send_message(callback.message.chat.id, str(delete_vm_info))
        start_message(callback.message)

    elif "delete-vm-set-org-set-cld-set-fldr-" in callback.data:
        instance_info = integrateYC.get_instances_list(access_token=iam_access_token, folder_id=str(callback.data).split("-")[-1])

        markup = types.InlineKeyboardMarkup()
        for instance in instance_info:
            id = str(instance)
            instance_dict = instance_info.get(instance)
            external_ip = instance_dict.get("external_ip")
            markup.add(types.InlineKeyboardButton(text=str(external_ip), callback_data="delete-vm-folder-id-" + id))
            
        return_button = types.InlineKeyboardButton("Return", callback_data="return")
        markup.add(return_button)

        bot.send_message(callback.message.chat.id, "Set instance", reply_markup=markup)
    elif "delete-vm-set-organization-set-cloud-" in callback.data:
        folders_info = integrateYC.get_folders(access_token=iam_access_token, cloud=str(callback.data).split("-")[-1])
        markup = types.InlineKeyboardMarkup()
        for folder in folders_info.get("folders"):
            button_name = str(folder.get("name"))
            button_callback = str("delete-vm-set-org-set-cld-set-fldr-" + folder.get("id"))
            markup.add(types.InlineKeyboardButton(text=button_name, callback_data=button_callback))
            
        return_button = types.InlineKeyboardButton("Return", callback_data="return")
        markup.add(return_button)

        bot.send_message(callback.message.chat.id, "Set folder", reply_markup=markup) 
    elif "delete-vm-set-organization" in callback.data:
        markup = types.InlineKeyboardMarkup()
        clouds_info = integrateYC.get_clouds(access_token=iam_access_token, organization=str(callback.data).split("-")[-1])
        for cloud in clouds_info.get("clouds"):
            markup.add(types.InlineKeyboardButton(text=str(cloud.get("name")), callback_data=str("delete-vm-set-organization-set-cloud-" + cloud.get("id"))))

        return_button = types.InlineKeyboardButton("Return", callback_data="return")
        markup.add(return_button)

        bot.send_message(callback.message.chat.id, "Set cloud", reply_markup=markup) 


@bot.callback_query_handler(func=lambda call: call.data.startswith("list-vms"))
def list_vms(callback):
    if "list-vms-set-org-set-cld-set-fldr-" in callback.data:
        instance_info = integrateYC.get_instances_list(access_token=iam_access_token, folder_id=str(callback.data).split("-")[-1])

        bot.send_message(callback.message.chat.id, str(instance_info))
        start_message(callback.message)

    elif "list-vms-set-organization-set-cloud-" in callback.data:
        folders_info = integrateYC.get_folders(access_token=iam_access_token, cloud=str(callback.data).split("-")[-1])
        markup = types.InlineKeyboardMarkup()
        for folder in folders_info.get("folders"):
            button_name = str(folder.get("name"))
            button_callback = str("list-vms-set-org-set-cld-set-fldr-" + folder.get("id"))
            markup.add(types.InlineKeyboardButton(text=button_name, callback_data=button_callback))
            
        return_button = types.InlineKeyboardButton("Return", callback_data="return")
        markup.add(return_button)

        bot.send_message(callback.message.chat.id, "Set folder", reply_markup=markup) 
    elif "list-vms-set-organization" in callback.data:
        markup = types.InlineKeyboardMarkup()
        clouds_info = integrateYC.get_clouds(access_token=iam_access_token, organization=str(callback.data).split("-")[-1])
        for cloud in clouds_info.get("clouds"):
            markup.add(types.InlineKeyboardButton(text=str(cloud.get("name")), callback_data=str("list-vms-set-organization-set-cloud-" + cloud.get("id"))))

        return_button = types.InlineKeyboardButton("Return", callback_data="return")
        markup.add(return_button)

        bot.send_message(callback.message.chat.id, "Set cloud", reply_markup=markup)   
    

@bot.callback_query_handler(func=lambda call: call.data.startswith("list-clouds"))
def list_clouds(callback):
    if "list-clouds-set-organization" in callback.data:
        clouds_info = integrateYC.get_clouds(access_token=iam_access_token, organization=str(callback.data).split("-")[-1])
        bot.send_message(callback.message.chat.id, str(clouds_info))
        start_message(callback.message)


@bot.callback_query_handler(func=lambda call: call.data.startswith("list-folders"))
def list_folders(callback):
    if "list-folders-set-organization-set-cloud-" in callback.data:
        folders_info = integrateYC.get_folders(access_token=iam_access_token, cloud=str(callback.data).split("-")[-1])

        bot.send_message(callback.message.chat.id, str(folders_info))
        start_message(callback.message)
    elif "list-folders-set-organization" in callback.data:
        markup = types.InlineKeyboardMarkup()
        clouds_info = integrateYC.get_clouds(access_token=iam_access_token, organization=str(callback.data).split("-")[-1])
        for cloud in clouds_info.get("clouds"):
            markup.add(types.InlineKeyboardButton(text=str(cloud.get("name")), callback_data=str("list-folders-set-organization-set-cloud-" + cloud.get("id"))))

        return_button = types.InlineKeyboardButton("Return", callback_data="return")
        markup.add(return_button)

        bot.send_message(callback.message.chat.id, "Set cloud", reply_markup=markup)
    

@bot.callback_query_handler(func=lambda call: call.data.startswith("stop-vm"))
def stop_instance(callback):
    if "stop-vm-id-" in callback.data:
        stop_vm_info = integrateYC.stop_vm(access_token=iam_access_token, vm_id=str(callback.data).split("-")[-1])

        bot.send_message(chat_id=callback.message.chat.id, text=str(stop_vm_info))
        start_message(callback.message)

    elif "stop-vm-set-org-set-cld-set-fldr-" in callback.data:
        instance_info = integrateYC.get_instances_list(access_token=iam_access_token, folder_id=str(callback.data).split("-")[-1])

        markup = types.InlineKeyboardMarkup()
        for instance in instance_info:
            id = str(instance)
            instance_dict = instance_info.get(instance)
            external_ip = instance_dict.get("external_ip")
            markup.add(types.InlineKeyboardButton(text=str(external_ip), callback_data="stop-vm-id-" + id))
            
        return_button = types.InlineKeyboardButton("Return", callback_data="return")
        markup.add(return_button)

        bot.send_message(callback.message.chat.id, "Set instance", reply_markup=markup)
    elif "stop-vm-set-organization-set-cloud-" in callback.data:
        folders_info = integrateYC.get_folders(access_token=iam_access_token, cloud=str(callback.data).split("-")[-1])
        markup = types.InlineKeyboardMarkup()
        for folder in folders_info.get("folders"):
            button_name = str(folder.get("name"))
            button_callback = str("stop-vm-set-org-set-cld-set-fldr-" + folder.get("id"))
            markup.add(types.InlineKeyboardButton(text=button_name, callback_data=button_callback))
            
        return_button = types.InlineKeyboardButton("Return", callback_data="return")
        markup.add(return_button)

        bot.send_message(callback.message.chat.id, "Set folder", reply_markup=markup) 
    elif "stop-vm-set-organization" in callback.data:
        markup = types.InlineKeyboardMarkup()
        clouds_info = integrateYC.get_clouds(access_token=iam_access_token, organization=str(callback.data).split("-")[-1])
        for cloud in clouds_info.get("clouds"):
            markup.add(types.InlineKeyboardButton(text=str(cloud.get("name")), callback_data=str("stop-vm-set-organization-set-cloud-" + cloud.get("id"))))

        return_button = types.InlineKeyboardButton("Return", callback_data="return")
        markup.add(return_button)

        bot.send_message(callback.message.chat.id, "Set cloud", reply_markup=markup) 


@bot.callback_query_handler(func=lambda call: call.data.startswith("start-vm"))
def stop_instance(callback):
    if "start-vm-id-" in callback.data:
        start_vm_info = integrateYC.start_vm(access_token=iam_access_token, vm_id=str(callback.data).split("-")[-1])

        bot.send_message(chat_id=callback.message.chat.id, text=str(start_vm_info))
        start_message(callback.message)

    elif "start-vm-set-org-set-cld-set-fldr-" in callback.data:
        instance_info = integrateYC.get_instances_list(access_token=iam_access_token, folder_id=str(callback.data).split("-")[-1])

        markup = types.InlineKeyboardMarkup()
        for instance in instance_info:
            id = str(instance)
            instance_dict = instance_info.get(instance)
            external_ip = instance_dict.get("external_ip")
            markup.add(types.InlineKeyboardButton(text=str(external_ip), callback_data="start-vm-id-" + id))
            
        return_button = types.InlineKeyboardButton("Return", callback_data="return")
        markup.add(return_button)

        bot.send_message(callback.message.chat.id, "Set instance", reply_markup=markup)
    elif "start-vm-set-organization-set-cloud-" in callback.data:
        folders_info = integrateYC.get_folders(access_token=iam_access_token, cloud=str(callback.data).split("-")[-1])
        markup = types.InlineKeyboardMarkup()
        for folder in folders_info.get("folders"):
            button_name = str(folder.get("name"))
            button_callback = str("start-vm-set-org-set-cld-set-fldr-" + folder.get("id"))
            markup.add(types.InlineKeyboardButton(text=button_name, callback_data=button_callback))
            
        return_button = types.InlineKeyboardButton("Return", callback_data="return")
        markup.add(return_button)

        bot.send_message(callback.message.chat.id, "Set folder", reply_markup=markup) 
    elif "start-vm-set-organization" in callback.data:
        markup = types.InlineKeyboardMarkup()
        clouds_info = integrateYC.get_clouds(access_token=iam_access_token, organization=str(callback.data).split("-")[-1])
        for cloud in clouds_info.get("clouds"):
            markup.add(types.InlineKeyboardButton(text=str(cloud.get("name")), callback_data=str("start-vm-set-organization-set-cloud-" + cloud.get("id"))))

        return_button = types.InlineKeyboardButton("Return", callback_data="return")
        markup.add(return_button)

        bot.send_message(callback.message.chat.id, "Set cloud", reply_markup=markup) 

    
@bot.callback_query_handler(func=lambda call: call.data.startswith("restart-vm"))
def stop_instance(callback):
    if "restart-vm-id-" in callback.data:
        restart_vm_info = integrateYC.restart_vm(access_token=iam_access_token, vm_id=str(callback.data).split("-")[-1])

        bot.send_message(chat_id=callback.message.chat.id, text=str(restart_vm_info))
        start_message(callback.message)

    elif "restart-vm-set-org-set-cld-set-fldr-" in callback.data:
        instance_info = integrateYC.get_instances_list(access_token=iam_access_token, folder_id=str(callback.data).split("-")[-1])

        markup = types.InlineKeyboardMarkup()
        for instance in instance_info:
            id = str(instance)
            instance_dict = instance_info.get(instance)
            external_ip = instance_dict.get("external_ip")
            markup.add(types.InlineKeyboardButton(text=str(external_ip), callback_data="restart-vm-id-" + id))
            
        return_button = types.InlineKeyboardButton("Return", callback_data="return")
        markup.add(return_button)

        bot.send_message(callback.message.chat.id, "Set instance", reply_markup=markup)
    elif "restart-vm-set-organization-set-cloud-" in callback.data:
        folders_info = integrateYC.get_folders(access_token=iam_access_token, cloud=str(callback.data).split("-")[-1])
        markup = types.InlineKeyboardMarkup()
        for folder in folders_info.get("folders"):
            button_name = str(folder.get("name"))
            button_callback = str("restart-vm-set-org-set-cld-set-fldr-" + folder.get("id"))
            markup.add(types.InlineKeyboardButton(text=button_name, callback_data=button_callback))
            
        return_button = types.InlineKeyboardButton("Return", callback_data="return")
        markup.add(return_button)

        bot.send_message(callback.message.chat.id, "Set folder", reply_markup=markup) 
    elif "restart-vm-set-organization" in callback.data:
        markup = types.InlineKeyboardMarkup()
        clouds_info = integrateYC.get_clouds(access_token=iam_access_token, organization=str(callback.data).split("-")[-1])
        for cloud in clouds_info.get("clouds"):
            markup.add(types.InlineKeyboardButton(text=str(cloud.get("name")), callback_data=str("restart-vm-set-organization-set-cloud-" + cloud.get("id"))))

        return_button = types.InlineKeyboardButton("Return", callback_data="return")
        markup.add(return_button)

        bot.send_message(callback.message.chat.id, "Set cloud", reply_markup=markup)


# --------------- local testing ---------------
if __name__ == "__main__":
    bot.infinity_polling()
