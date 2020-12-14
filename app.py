from SOR_SCRIPT import NER

import streamlit as st 


st.title('**Soul of Reason**')
st.markdown(""" #### Named entity recognition of the "Soul of Reason" radio program transcripts. """)

st.text("")
st.text("")

st.sidebar.markdown("### Input data folder and metadata below:")

path_ = st.sidebar.text_input("Enter Text Folder Path:")

met_path = st.sidebar.file_uploader("Drag and Drop Metadata [.csv] File:", type="csv")


if (st.sidebar.button("Run")) and (path_ is not None) and (met_path is not None):

	cls = NER()

	with st.spinner('Importing text files...'):
		corpus = cls.import_txt_files(path_)
	with st.spinner('Removing timestamps...'):
		corp_clean = cls.remove_timestamps(corpus)
	with st.spinner('Linking Metadata...'):
		corp_met = cls.link_metadata(corp_clean, path_)
	with st.spinner('Predicting Entities...'):
		ents = cls.predict_entities(corp_met)
	with st.spinner('Creating Final Dataset...'):
		final = cls.create_final_dataset(ents[0], met_path)


	st.balloons()
	st.markdown(""" ### Check your current directory for the CSV and JSON files!""")