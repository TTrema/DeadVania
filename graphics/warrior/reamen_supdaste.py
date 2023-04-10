import os

# Obter o caminho da pasta atual
root_path = os.getcwd()

# Percorrer todas as subpastas na pasta atual
for subdir_name in os.listdir(root_path):
    # Verificar se o item na pasta atual é uma subpasta
    if os.path.isdir(os.path.join(root_path, subdir_name)):
        # Renomear a subpasta para ter um nome em minúsculas
        os.rename(os.path.join(root_path, subdir_name), os.path.join(root_path, subdir_name.lower()))
