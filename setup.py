import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="biology_revision_project",
    version="0.0.1",

    description="An empty CDK Python app",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="author",

    package_dir={"": "biology_revision_project"},
    packages=setuptools.find_packages(where="biology_revision_project"),

    install_requires=[
        "aws-cdk.core==1.118.0",
        "aws-cdk.aws-lambda==1.118.0",
        "aws-cdk.aws-apigateway==1.118.0",
        "aws-cdk.aws-rds==1.118.0",
        "aws-cdk.aws-route53-targets==1.118.0",
        "aws-cdk.aws-ec2==1.118.0",
        "aws-cdk.aws-lambda-python==1.118.0",
        "aws-cdk.aws-s3==1.118.0",
        "aws-cdk.aws-s3-deployment==1.118.0",
        "psycopg2-binary==2.9.1"
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
