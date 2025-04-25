# RacJac
Project RacJac is the project where I, for say, gave the job description as an input and/or any other inputs in form of arguments like yes/no, it asks me to provide them. Then Outputs pdf of resume developed

## Inputs
inputs should be added in the **Data** folder.
- dex.yaml is where you add your resume details
- jd.txt is where you add job description

## Scripts
### Extract
This is where we parse the yaml doc while extracting from the above input file(dex.yaml)

### Organizer
This is like a closet of classes, where everything is organized as per the model classes here

### Doc
Here is where, the extracted data which was converted into **resume** object is used to fit into the template
#### Utils
Helper file is used to write different method for converting each object into html format

### Gen
Work need to be done.

### Template
Here you can find html template and css styles used to create resume as pdf.
