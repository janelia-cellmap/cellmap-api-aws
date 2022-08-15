#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cellmap_api_aws.cellmap_api_aws_stack import CellmapApiAwsStack


app = cdk.App()
CellmapApiAwsStack(app, "CellmapApiAwsStack", public=True)
app.synth()
