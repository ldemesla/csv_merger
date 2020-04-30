# CSV MERGER

## usage

`./csv_merger [model_file] [csv_1] [csv_2] ...`

The first argument must be a model file following this format defined in the `model.txt` file provided in `data`, this file is going to define the format of the outputed CSV file, you can specify key for correspondence and also synonyme to perform merging even if the column names are not the same. The following arguments are the CSV files that need to be merged, each file as a priority defined by is position in the argument list, so the first CSV file argument is the one with the highest priority, which mean that is two row in two different file, share the same key, but also entries that do not match, then the program will choose the entrie with the highest priority.

`srcs/test.py` launch unit testing
