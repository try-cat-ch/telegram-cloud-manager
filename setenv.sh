echo "export BOT_TOKEN_LOCAL="$(pass ls telegram-cloud-manager/bot_token_dev)"" >> ~/.bashrc
echo "export BOT_TOKEN_PROD="$(pass ls telegram-cloud-manager/bot_token_prod)"" >> ~/.bashrc
echo "export USER_ID_ADMIN="$(pass ls telegram-cloud-manager/user_id_try_cat_ch)"" >> ~/.bashrc

echo "export CLOUD_ID="$(pass ls telegram-cloud-manager/tinder/main/cloud_id)"" >> ~/.bashrc
echo "export FOLDER_ID="$(pass ls telegram-cloud-manager/tinder/main/folder_id)"" >> ~/.bashrc
echo "export SUBNET_ID="$(pass ls telegram-cloud-manager/tinder/main/subnet_id)"" >> ~/.bashrc
echo "export IMAGE_ID="$(pass ls telegram-cloud-manager/tinder/main/image_id)"" >> ~/.bashrc

echo "export YC_SERVICE_ACCOUNT_ID="$(pass ls telegram-cloud-manager/tinder/main/yc_service_account_id)"" >> ~/.bashrc
echo "export YC_SERVICE_ACCOUNT_KEY_ID="$(pass ls telegram-cloud-manager/tinder/main/yc_service_account_key_id)"" >> ~/.bashrc
echo -e $(pass ls telegram-cloud-manager/tinder/main/id_rsa_pk_service_account_bot_account) > key.txt
