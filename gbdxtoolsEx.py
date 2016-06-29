from gbdxtools import Interface

gbdx=Interface() # Instantiate gbdxtools, which logs you in using your .config file


#### SEARCHING THE CATALOG WITH FILTERS

wkt_string = "POLYGON((-122.43434482199342028 47.69012820633496119,-122.24650297391180231 47.6831711008504584,-122.23954586842728531 47.49532925276882622,-122.41347350553991191 47.49532925276882622,-122.43434482199342028 47.69012820633496119))"

filters = filters = [
        "(sensorPlatformName = 'WORLDVIEW03' OR sensorPlatformName ='WORLDVIEW02')",
        "cloudCover < 10",
        "offNadirAngle < 10"
]

results = gbdx.catalog.search(searchAreaWkt=wkt_string,
                          startDate="2004-01-01T00:00:00.000Z",
                          endDate="2016-01-01T00:00:00.000Z",
                          filters=filters)

catalog_ids = [r['identifier'] for r in results] #Save catIDs in a list to use to find s3 locations
print catalog_ids


#### RUNNING WORKFLOWS

workflowList = [] # We will keep track of our workflows by putting workflow IDs in a list as they are created

for catID in catalog_ids: # Loop through all of the catIDs we found earlier to find their s3 location. This will be the input for the first task.
	s3path = gbdx.catalog.get_data_location(catalog_id=catID)
	print s3path

	if s3path!= None:
		s3path = '/'.join(s3path.split('/')[:-1])+'/'
		print s3path

		aoptask = gbdx.Task("AOP_Strip_Processor", data=s3path, enable_acomp=True, enable_pansharpen=False, enable_dra=False, bands='MS')
		s3task = gbdx.Task("StageDataToS3")
		s3task.inputs.data = aoptask.outputs.data.value
		s3task.inputs.destination = "s3://molly-g/seattleAOP/"

		pp_task = gbdx.Task("ProtogenPrep",raster=aoptask.outputs.data.value)      # ProtogenPrep task is used to get AOP output into proper format for protogen task
		prot_ubfp = gbdx.Task("protogenV2UBFP", raster=pp_task.outputs.data.value)
		workflow = gbdx.Workflow([ pp_task, aoptask, prot_ubfp, s3task ]) # Cool tip: these can be in any order!
		workflow.savedata(prot_ubfp.outputs.data.value, location="/molly-g/seattle") # 'location' should be your subdirectory in your bucket prefix
		workflow.execute() 
		workflowList.append(workflow.id)

print workflowList

for wfID in workflowList:
	status = gbdx.workflow.status(wfID)
	print status
