import requests, json
import getopt, sys
import config

def upload_imagga(image_path): 
        #api_key = 'acc_43a212cace97cc9'
	#api_secret = 'a91461f1c5022a79b419f453e6a14aff'
 		
	response = requests.post('https://api.imagga.com/v2/uploads',
                                 auth=(config.api_key, config.api_secret),
                                 files={'image': open(image_path, 'rb')})
        if (response.json()['status']['type'] == 'success'):
                print ('\t Upload successful')
                upld_id = response.json()['result']['upload_id']
                return (upld_id)
        else:
                print('\t Something went wrong. Exiting...')
                sys.exit(2)
        

def tag_imagga(t_image):
	response = requests.get('https://api.imagga.com/v2/tags?image_upload_id=%s' % t_image,
                                auth=(config.api_key, config.api_secret))
        if (response.json()['status']['type'] == 'success'):
            print ('\t Tagging successful')
            return(response.json())
        else:
                print('\t Something went wrong. Exiting...')
                sys.exit(2)
        

def delete_imagga(upld_id):
	response = requests.delete('https://api.imagga.com/v2/uploads/%s'
                                   % (upld_id), auth=(config.api_key, config.api_secret))
	if (response.json()['status']['type'] == 'success'):
            print ('\t Delete successful')
            return(response.json())
        else:
                print('\t Something went wrong. Exiting...')
                sys.exit(2)
        
	
def main(argv):
        try:
                opts, args = getopt.getopt(argv,"i:", ["image="]) 
	except getopt.GetoptError:
                print ('Usage: python tagging.py --image=<image_path>')
                sys.exit(2)
        req_options = 0
	for opt, arg in opts:
                       if opt == '--image':
                               t_image = arg
                               req_options = 1

        if (req_options == 0):
                print ('Usage: python tagging.py --image=<image_path>')
                sys.exit(2)
                        
	# Upload the image 
        print('Uploading image to Imagga: ', t_image)
	upld_id = upload_imagga(t_image)
	
	# Tag the image 
	print('Tagging the image:')
	tags_json = tag_imagga(upld_id)

	## Parse the tags
	num_tags = len(tags_json['result']['tags'])
        tags_to_print = min(num_tags,5)
        print ('\t Top tags (confidence score):')
	for i in range(tags_to_print):
                       print('\t {} {}'.format(str(tags_json['result']['tags'][i]['tag']['en']),
                             round(tags_json['result']['tags'][i]['confidence'],1)))
                
        
	# Delete the image
        print('Deleting image from Imagga:')
	delete_imagga(upld_id)


	
if __name__ == "__main__":
   main(sys.argv[1:])
