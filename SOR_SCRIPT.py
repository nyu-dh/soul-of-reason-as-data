import glob
import os
import random
import spacy
import re
import warnings
import pandas as pd
from spacy import displacy
from tqdm import trange
from tqdm import tqdm
from itertools import chain
from pathlib import Path

class NER:
    
    def __init__(self):
        self.nlp = spacy.load('en')
        
        
    def import_txt_files(self, path):
        """ 
        
        Loads a series of text files into Python. 
    
        Input
        -----------------------------------------
        path : string
            This is the directory path to your folder of text files. Note that the path must be in single ('') 
            or double ("") quotations. To avoid confusion during processing, this directory should only contain
            the text files that you want to analyze for entities.
        
            Example - 
        
                    '/Users/myusername/Desktop/soul-of-reason-as-data/data' 
                    (where /data is the folder containing all text files)


        Returns
        -----------------------------------------
        corpus : list 
            Returns a Python list of all of the text files, as well as the total number of documents in the corpus 
            (the number of text files in your folder).


        """
        
        print("Importing text files...")
        
        # Compile all text file names from working directory
        
        txt_files = glob.glob(os.path.join(os.getcwd(), path, "*.txt"))
        
        # Append each document to a list called corpus + error-handle

        corpus = []
        
        try:
            for individual_file in txt_files:
                with open(individual_file) as f_input:
                    corpus.append(f_input.read())
        except:
            print("ERROR: Could not import text files. Please ensure that you entered that correct directory path "+
                  "and that all of the files you want to analyze have a .txt extension.")
            
                
        # Return the number of documents in the corpus & the Python corpus list

        print("Number of documents in corpus: ",len(corpus))

        return corpus
    
    
    def remove_timestamps(self, docs):
        """
        
        Removes timestaps (i.e. - 'Dr. Roscoe C Brown 00:00:01.490') from text. This ensures that the model does 
        not repeatedly include these entities in the final dataset. 
        
        Input 
        -----------------------------------------
        text : list
            The list of documents you want to remove timestamps from; i.e. the output from import_txt_files().
            
            
        Returns
        -----------------------------------------
        docs : list
            The same list of documents from the input, except with all timestamps removed. 
        
        """
        
        print("Removing timestamps...")
        
        # Find all transcription lines using regex (must convert to string/non-list item first)
        
        text = ''.join(docs)
        lines = re.findall("[0-9][0-9].[0-9][0-9].[0-9][0-9].[0-9][0-9][0-9]*", text)
        
        # Error handle -- return message if there are no transcription lines to be found
        
        if len(lines) == 0:
            print("ERROR: No transcription lines have been found in the corpus. Did you remove them already? If so, "+
                 "you don't need to use this function and can skip to link_metadata.")
        else:
            
            # Split lines + replaced double-spaced lines with single spaced lines

            split = text.replace('\n\n','\n').splitlines() 

            # Append all of the transcription lines to a list

            lines_remove = []                  
            for i in split:
                for j in lines:
                    if j in i:
                        lines_remove.append(i)

            # Remove aforementioned trancription lines

            for i in range(len(docs)):          
                for j in lines_remove:
                    if j in docs[i]:
                        docs[i] = docs[i].replace(j,'')

            # Replace double-lines with single & triple lines with double

            for i in range(len(docs)):
                docs[i] = docs[i].replace('\n\n','')    

            print("Timestamps removed from corpus.")       
        
        return docs
    
    
    def link_metadata(self, docs, txt_path):
        """
        
        Links the text file name (e.g. 'RG_9_8_208.txt') to the corresponding text document in Python.

        NOTE: 
            - This function is dependent on the fact that each text file is named in a format similar to 
             'RG_9_8_208.txt' or 'RG9-8_ref4330.txt' (for example). Text files that do not meet either of 
              these naming formats will not be identified and an error will be thrown, with a reference to 
              the invalid document(s).

            - Please also ensure that the text files in your txt_path are only those you want to analyze 
              (i.e. no irrelevant text files).

            - Running this function multiple times in the same class instance will result in the metadata 
              being appended more than once. 

        Input
        -------------------------
        docs : list
            The list of all documents where metadata needs to be appended, i.e. the 'docs' output from 
            remove_timestamps(). The number of documents in this list should match the number of documents 
            imported after using import_txt_files().  

        txt_path : string
            The directory path on your computer where all .txt files are stored; this should be the same as that 
            used in import_txt_files(). Note that the path must be in single ('') or double ("") quotations.

            Example - 

            '/Users/myusername/Desktop/soul-of-reason-as-data/data' 
            (where /data is the folder containing all text files)

        Returns
        ------------------------
        docs : list
            The same list you inputted, except with an appended reference to the corresponding file name at the end 
            of every document, in the form of: <DOC_ID>: 'text file name.'

        """
        
        print("Adding metadata identifier to each document...\n\n")
        
        # Create list of text file names from txt_path
        
        txt_files = glob.glob(os.path.join(os.getcwd(), txt_path, "*.txt"))
        
        # Create four empty lists to collect the file names for each document
        # There are four lists because there are four 'types' of naming formats
        # l1 will be the final list (other lists will be merged into this one)
        # Therefore, make l1 a global variable because it will be used in another function

        global l1 
        l1 = []
        l2 = []
        l3 = []
        l4 = []

        # Find all names of text files using regex, following the given formats (mentioned in docstring)
        
        for i in range(len(txt_files)):   
            l1.append(re.findall('[A-Z][A-Z]\w[0-9]\w[0-9]\w[0-9][0-9][0-9]\W[a-z][a-z][a-z]',txt_files[i]))
            l2.append(re.findall('[A-Z][A-Z]\w[0-9]\w[0-9]\w[0-9][0-9]\W[a-z][a-z][a-z]',txt_files[i]))
            l3.append(re.findall('[A-Z][A-Z][0-9]\W[0-9]\w[a-z][a-z][a-z][0-9][0-9][0-9][0-9]\W[a-z][a-z][a-z]', txt_files[i]))
            l4.append(re.findall('[A-Z][A-Z][0-9]\w[0-9]\w[0-9][0-9][0-9]\W[a-z][a-z][a-z]',txt_files[i]))
        
        # Merge the lists of the text file names to get one complete list, l1
        
        for i in range(len(l1)):         
            if l1[i] == [] and l2[i] != []:
                l1[i] = l2[i]
            elif l1[i] == [] and l3[i] != []:
                l1[i] = l3[i]
            elif l1[i] == [] and l4[i] != []:
                l1[i] = l4[i]
            else:
                pass
            
        # Add the corresponding .txt file name to the end of each document (+ error handling)
        # A message will appear if files do not file the given naming format (as given by the digi_id of metadata)
        # A message will appear if you have extra text files in your directory path
        # This <DOC_ID> will be called to link the metadata file when creating the final dataset

        empties = []    
        if len(docs) == len(l1):
            for i in tqdm(range(len(docs))):
                docs[i] = docs[i] + ' <DOC_ID>: '+''.join(l1[i])
            print("Finished linking metadata. Each document in the corpus list contains a <DOC_ID> identifier on the last "\
                  "line, with its corresponding .txt file name.\n\n")
        else:
            if [] in l1:
                for i in range(len(l1)):
                    if l1[i] == []:
                        empties.append(i)
                    empty_docs = [txt_files[x] for x in empties]
                print("ERROR: One or more .txt document names could not be found. Please ensure that the names of all .txt "+
                "files follow the permitted naming format. Error comes from document(s): ",empties,empty_docs)
            else:
                print("ERROR: The number of text files in your directory path does not equal the number of text files imported!\n"+
                      "Please ensure there are no additional .txt files in the file path you supplied.\n\n")

        return docs
    

    def predict_entities(self, corpus):
        """
        
        Predicts entities in the given corpus. Entities are labelled according to spaCy entitiy types; see 
        https://spacy.io/api/annotation#named-entities for a list of all labels.
        
        NOTE:
            - Remember that this function has two outputs (described below). The next function takes only the FIRST
              ouptut of this function, therefore you will need to index this function's output by [0].
        
        Input
        ----------------------------------------
        corpus : list
            The list of documents to extract entities from; this should be the output from link_metadata().
            
        Returns
        ----------------------------------------
        preds : list
            A list of tuples in the form of [(Entity, Start_Index, End_Index, Entity_Label, Doc_ID)], predicted 
            by the spaCy model. This will be passed as input to the create_final_dataset() function.
            
        ents_only : list
            A list of *only* the predicted entities; includes duplicates and predicted entities from every document.
            This output is not used in any other function; it is returned as a supplementary list that could be 
            useful for further analysis in Python.
        
        """
        
        print("Predicting entitiies...")
        
        # Extract <DOC_ID> tokens & append to list, doc_ids
        # Use the index -17 because the <DOC_ID> token will be the very last token (hence, the negative)
        # 17 is used because, according to the given format, the longest document id would be 17 characters
        
        preds = []
        doc_ids = []
        ents_only = []
        
        for i in range(len(corpus)):
            doc = corpus[i]
            doc_id = doc[-17:]
            doc_ids.append(doc_id)
        
        # Remove extra characters from doc_ids list --> remove 'D>:' and '>:' which may have been included
        # ... becauase of the <DOC_ID> part
        # This applies to file names that are less than 17 characters 
        
        for i in range(len(doc_ids)):
            doc_ids[i] = doc_ids[i].replace('D>: ','')
            doc_ids[i] = doc_ids[i].replace('>: ','')
        
        # Predict entities, append information to a list called preds + error handling
        # Predictions made using spaCy's pre-trained model, which I named 'nlp' (see the init method) 
        
        try:
            for i in tqdm(range(len(corpus))):
                doc = corpus[i]
                preproc_doc = self.nlp(doc)
                for ent in preproc_doc.ents:
                    preds.append((ent.text, ent.start_char, ent.end_char, ent.label_, doc_ids[i]))
                    ents_only.append(ent.text)
        except:
            print("ERROR: Could not predict all entities. Please ensure you are using the correct input to this function.\n\n")


        return preds, ents_only

    
    def create_final_dataset(self, preds, metadata_path, *args):
        """
        
        Creates the final dataset of named entities, and downloads this dataset to your current working directory
        as both a csv and json file. 
        
        NOTE:
            - This function requires the column containing the text file names in the metadata file to be 
              called 'digi_id'
            - If you choose to include the *args option (see description below), note that it must come 
              after the 'metadata_path' argument. 
            - Remember that you should only be using the first output from predict_entities() as input to this
              function. This means you need to index the ouptut from predict_entities() by [0].
        
        Input
        ----------------------------------
        preds : list (required)
            The list of tuples in the form of [(Entity, Start_Index, End_Index, Entity_Label, Doc_ID)]. This should
            be the output from the predict_entities() function.
            
        metadata_path : string (required)
            The file path containing the metadata file of your corpus. Note that this should be the *file* path and 
            not the *folder* path. 
            
        *args : list (optional)
            The list of entity types you want to filter by. This is an optional argument that allows you to choose 
            which entity types you want to see; i.e. - ['PERSON', 'ORG'] will return/save a dataset containing only
            entities identified as a person or organization. 
            
        
        Returns
        ----------------------------------
        final_df : pandas DataFrame
            The final dataset of named entities, containing the entity, its start & end Python index, its entity 
            type, and all corresponding inputted metadata from the metadata file path.
            
        This function also returns both a csv and a json file with the same information as that in final_df above. 
        These datasets are automatically downloaded to your current working directory.
            
        """
        
        print("Creating final dataset...\n\n")
        
        # Make dataset, name columns
        
        cols = ['Entities','Start_index','End_index','Label','Doc_ID']
        df = pd.DataFrame(preds,columns=cols)
        
        # Drop 'DOC_ID' string & possible text file names picked up as entities
        # For example, 'RG_9_8_110' may be a record in the dataset labelled as CARDINAL
        
        df = df[~df['Entities'].isin(['DOC_ID'])]
        df = df[~df['Entities'].isin(l1)]
        
        # Drop '.txt' at the end of Doc_ID column, so that only the digi ids are reflected
        
        df['Doc_ID'] = df['Doc_ID'].replace(to_replace=r'\.txt', value='', regex=True)
        
        # Read in metadata file
        
        metadata = pd.read_csv(metadata_path)
        
        # Option to filter dataset by entitiy type
        
        if args:
            my_ents = list(chain(*args))
            try:
                df = df[df['Label'].isin(my_ents)]
            except:
                print("ERROR: could not filter by the inputted entitiy types. Please ensure each of your entity "+
                     "types is correct & exactly matches the spaCy formatting. See "+
                      "https://spacy.io/api/annotation#named-entities for a list of all available entity types.\n\n")
        
        # Link metadata file with entity dataset
        
        try:
            metadata = metadata.rename(columns={"digi_id":'Doc_ID'})
            final_df = pd.merge(df, metadata, how='inner', on='Doc_ID')
        except:
            print("ERROR: Could not link metadata to entity dataset. Please ensure that the column name 'digi_id' (the "+
                 "column containg the text file names), is present in the metadata file.\n\n")
        
        # Save dataset as csv to current directory
        
        final_df.to_csv('named_entities_csv.csv',index=False)
        final_df.to_json('named_entities_json.json', orient='columns')
        
        print("The named entity datastets, 'named_entities_csv' and 'named_entities_json', have been saved to your "+
              "current working \ndirectory.\n\n")
        
        # Give number of unique labels identified
        
        print("\nNumber of unique entities identified:",len(final_df['Entities'].unique()),"\n\n\nNumber of entities "+ 
              "identified, by entitiy type:\n",final_df['Label'].value_counts())
         
        return final_df

def main():
    cls = NER()
    path_ = str(input("Please enter the name of the folder path to your text files: "))
    corpus = cls.import_txt_files(path_)
    corp_clean = cls.remove_timestamps(corpus)
    corp_met = cls.link_metadata(corp_clean, path_)
    ents = cls.predict_entities(corp_met)
    met_path = str(input("Please enter the name of the file path to your metadata: "))
    final = cls.create_final_dataset(ents[0], met_path)
    
  
if __name__ == "__main__":
    main()