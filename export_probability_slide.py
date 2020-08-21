import os
import argparse
import pickle
import json

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--picklefolder", type=str, help="path to the folder containing pickles")
	parser.add_argument("--outputdir", type=str, help="path to the folder containing pickles")
	args = parser.parse_args()

	PICKLEDIR = args.picklefolder
	positions_in_slide = dict()
	

	#check every pickle file, 1 pickle = 1 slide
	for pkl in os.listdir(PICKLEDIR):
		patch_dic = dict()
		#load the slide's pickle
		with open(os.path.join(PICKLEDIR, pkl), "rb") as f_pkl:
			pickle_file = pickle.load(f_pkl)
			
		#for each patch in slide's pickle	
		for cle in pickle_file.keys():
			print(cle)
			_ , _ , slidename, x, y, level = cle.rsplit("_")
			# create a small dictionnary with patch name as key, containing a dictionnary with x, y and features info  
			patch_dic.update({cle : {'x' : int(x), 'y': int(y), 'feature' : (pickle_file[cle][0][0],pickle_file[cle][0][1]), 'var' : (pickle_file[cle][1][0],pickle_file[cle][1][1])} })
		

		#save json file for each slide
		name = str(pkl[:-2]+'.json')
		
		with open(os.path.join(args.outputdir,name), 'w') as fp:
			json.dump(patch_dic, fp)

		positions_in_slide.update({pkl[:-2] : patch_dic})

	#save as json file a dictionnary containing everything from picklefolder
	with open(os.path.join(args.outputdir,'positions_in_slide.json'), 'w') as f:
		json.dump(positions_in_slide, f)