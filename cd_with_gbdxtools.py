from gbdxtools import Interface

gbdx=Interface() # Instantiate gbdxtools, which logs you in using your .config file

s3path1 = 's3://receiving-dgcs-tdgplatform-com/055364007010_01_003'
aoptask1 = gbdx.Task("AOP_Strip_Processor", data=s3path1, enable_acomp=True, enable_pansharpen=False, enable_dra=False, bands='MS')
s3task1 = gbdx.Task("StageDataToS3")
s3task1.inputs.data = aoptask1.outputs.data.value
s3task1.inputs.destination = "s3://change_detection/test_job/Steps/acomp_fastortho_step-pre_image_task/Output"


s3path2 = 's3://receiving-dgcs-tdgplatform-com/055364005010_01_003'
aoptask2 = gbdx.Task("AOP_Strip_Processor", data=s3path2, enable_acomp=True, enable_pansharpen=False, enable_dra=False, bands='MS')
s3task2 = gbdx.Task("StageDataToS3")
s3task2.inputs.data = aoptask1.outputs.data.value
s3task2.inputs.destination = "s3://change_detection/test_job/Steps/acomp_fastortho_step-post_image_task/Output"

cdtask = gbdx.Task("change_detection")
cdtask.inputs.pre_image = aoptask1.outputs.data.value
cdtask.inputs.post_image = aoptask2.outputs.data.value

workflow = gbdx.Workflow([ aoptask1, aoptask2, s3task1, s3task2, cdtask ])
workflow.savedata(cdtask.outputs.cd_output.value, location="change_detection/test_job/Steps/change_detection-singleton/Output")


'''

JSON version:

{
    "name": "3d33bfa2-4ea6-42d5-8101-17dcfa6bf785",
    "tasks": [
        {
            "containerDescriptors": [
                {
                    "properties": {
                        "domain": "raid"
                    }
                }
            ],
            "inputs": [
                {
                    "name": "enable_dra",
                    "value": "false"
                },
                {
                    "name": "bands",
                    "value": "MS"
                },
                {
                    "name": "enable_acomp",
                    "value": "true"
                },
                {
                    "name": "ortho_pixel_size",
                    "value": "2.0"
                },
                {
                    "name": "ortho_epsg",
                    "value": "EPSG:32636"
                },
                {
                    "name": "enable_pansharpen",
                    "value": "false"
                },
                {
                    "name": "data",
                    "value": "s3://receiving-dgcs-tdgplatform-com/055364007010_01_003"
                },
                {
                    "name": "ortho_dem_specifier",
                    "value": "SRTM90"
                }
            ],
            "name": "AOP_Strip_Processor_1fd51e39-a334-4a13-8fa6-b19cfe1c4f8c",
            "outputs": [
                {
                    "name": "data"
                },
                {
                    "name": "log"
               }
            ],
            "taskType": "AOP_Strip_Processor",
            "timeout": 36000
        },
        {
            "containerDescriptors": [
                {
                    "properties": {
                        "domain": "default"
                    }
                }
            ],
            "inputs": [
                {
                    "name": "destination",
                    "value": "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/change_detection/test_job/Steps/acomp_fastortho_step-pre_image_task/Output"
                },
                {
                    "name": "data",
                    "source": "AOP_Strip_Processor_1fd51e39-a334-4a13-8fa6-b19cfe1c4f8c:data"
                }
            ],
            "name": "StageDataToS3_71d5e169-19c1-4efb-9b6f-ddcf9f5bfa79",
            "outputs": [],
            "taskType": "StageDataToS3",
            "timeout": 7200
        },
        {
            "containerDescriptors": [
                {
                    "properties": {
                        "domain": "default"
                    }
                }
            ],
            "inputs": [
                {
                    "name": "destination",
                    "value": "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/change_detection/test_job/Steps/acomp_fastortho_step-pre_image_task/Log"
                },
                {
                    "name": "data",
                    "source": "AOP_Strip_Processor_1fd51e39-a334-4a13-8fa6-b19cfe1c4f8c:log"
                }
            ],
            "name": "StageDataToS3_06a1f8b2-7104-4c77-81e5-b4870861a18e",
            "outputs": [],
            "taskType": "StageDataToS3",
            "timeout": 7200
        },
        {
            "containerDescriptors": [
                {
                    "properties": {
                        "domain": "raid"
                    }
                }
            ],
            "inputs": [
                {
                    "name": "enable_dra",
                    "value": "false"
                },
                {
                    "name": "bands",
                    "value": "MS"
                },
                {
                    "name": "enable_acomp",
                    "value": "true"
                },
                {
                    "name": "ortho_pixel_size",
                    "value": "2.0"
                },
                {
                    "name": "ortho_epsg",
                    "value": "EPSG:32636"
                },
                {
                    "name": "enable_pansharpen",
                    "value": "false"
                },
                {
                    "name": "data",
                    "value": "s3://receiving-dgcs-tdgplatform-com/055364005010_01_003"
                },
                {
                    "name": "ortho_dem_specifier",
                    "value": "SRTM90"
                }
            ],
            "name": "AOP_Strip_Processor_26e0e139-9c2f-4049-9306-53b784176fac",
            "outputs": [
                {
                    "name": "data"
                },
                {
                    "name": "log"
                }
            ],
            "taskType": "AOP_Strip_Processor",
            "timeout": 36000
        },
        {
            "containerDescriptors": [
                {
                    "properties": {
                        "domain": "default"
                    }
                }
            ],
            "inputs": [
                {
                    "name": "destination",
                    "value": "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/change_detection/test_job/Steps/acomp_fastortho_step-post_image_task/Output"
                },
                {
                    "name": "data",
                    "source": "AOP_Strip_Processor_26e0e139-9c2f-4049-9306-53b784176fac:data"
                }
            ],
            "name": "StageDataToS3_decca798-ca89-45d6-b835-560e86b5d77a",
            "outputs": [],
            "taskType": "StageDataToS3",
            "timeout": 7200
        },
        {
            "containerDescriptors": [
                {
                    "properties": {
                        "domain": "default"
                    }
                }
            ],
            "inputs": [
                {
                    "name": "destination",
                    "value": "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/change_detection/test_job/Steps/acomp_fastortho_step-post_image_task/Log"
                },
                {
                    "name": "data",
                    "source": "AOP_Strip_Processor_26e0e139-9c2f-4049-9306-53b784176fac:log"
                }
            ],
            "name": "StageDataToS3_cf8040e3-c4a0-4c0b-8cbf-9e0cca12d5f6",
            "outputs": [],
            "taskType": "StageDataToS3",
            "timeout": 7200
        },
        {
            "containerDescriptors": [
                {
                    "properties": {
                        "domain": "default"
                    }
                }
            ],
            "inputs": [
                {
                    "name": "pre_image",
                    "source": "AOP_Strip_Processor_1fd51e39-a334-4a13-8fa6-b19cfe1c4f8c:data"
                },
                {
                    "name": "post_image",
                    "source": "AOP_Strip_Processor_26e0e139-9c2f-4049-9306-53b784176fac:data"
                }
            ],
            "name": "change_detection_90d49067-fdc7-413e-87d4-2259135da127",
            "outputs": [
                {
                    "name": "cd_output"
                }
            ],
           "taskType": "change_detection",
            "timeout": 36000
        },
        {
            "containerDescriptors": [
                {
                    "properties": {
                        "domain": "default"
                    }
                }
            ],
            "inputs": [
                {
                    "name": "destination",
                    "value": "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/change_detection/test_job/Steps/change_detection-singleton/Output"
                },
                {
                    "name": "data",
                    "source": "change_detection_90d49067-fdc7-413e-87d4-2259135da127:cd_output"
                }
            ],
            "name": "StageDataToS3_9561147a-0c10-4e6f-b762-9c924107571c",
            "outputs": [],
            "taskType": "StageDataToS3",
            "timeout": 7200
        }
    ]
}
'''