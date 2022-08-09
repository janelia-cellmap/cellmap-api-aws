import aws_cdk as core
import aws_cdk.assertions as assertions

from cellmap_api_aws.cellmap_api_aws_stack import CellmapApiAwsStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cellmap_api_aws/cellmap_api_aws_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CellmapApiAwsStack(app, "cellmap-api-aws")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
