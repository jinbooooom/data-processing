import os

savetxt_path = './savetxt'
modifytxt_path = './modifytxt'


txts = sorted(os.listdir(savetxt_path))

for txt in txts:
	txt_path = os.path.join(savetxt_path,txt)
	modify_path = os.path.join(modifytxt_path,txt)
	with open(txt_path,'r') as f1:
		with open(modify_path,'w') as f2:
			f2.write(f1.read().lower())
