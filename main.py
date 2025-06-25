import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

st.title("Data Preprocessor V1")

if 'df' not in st.session_state:
    st.header("Upload CSV file")
    uploaded_file = st.file_uploader("upload a csv file", type=["csv"])
    if uploaded_file is not None:
        st.write("File name:", uploaded_file.name)
        st.session_state.df = pd.read_csv(uploaded_file)

if 'df' in st.session_state:
    st.header("File sample")
    if st.button("Show !"):
        st.table(st.session_state.df.head(10))
    
    st.header("Drop columns")
    drop_form = st.form("drop cols")
    cols_to_drop = [[col, drop_form.checkbox(col, key=f"drop{i}")] for i, col in enumerate(st.session_state.df.columns)]
    if drop_form.form_submit_button("Drop !"):
        st.session_state.df.drop([x[0] for x in cols_to_drop if x[1]], axis=1, inplace=True)
        st.rerun()
    
    st.header("Drop null rows")
    drop_rows_form = st.form("drop rows")
    cols_to_drop_from = [[col, drop_rows_form.checkbox(col, key=f"droprow{i}")] for i, col in enumerate(st.session_state.df.columns)]
    if drop_rows_form.form_submit_button("Drop !"):
        st.session_state.df.dropna(subset=[x[0] for x in cols_to_drop_from if x[1]], inplace=True)
        st.rerun()
    
    st.header("Convert to category")
    convert_form = st.form("convert form")
    cols_to_convert = [[col, convert_form.checkbox(col, key=f"convert{i}")] for i, col in enumerate(st.session_state.df.columns)]
    if convert_form.form_submit_button("Convert"):
        st.session_state.df[[x[0] for x in cols_to_convert if x[1]]] = st.session_state.df[[x[0] for x in cols_to_convert if x[1]]].astype('category')
        st.rerun()

    st.header("Replace nulls")
    replace_nulls_form = st.form("replace nulls")
    cols_to_fill = [[col, replace_nulls_form.checkbox(col, key=f"fillcol{i}")] for i, col in enumerate(st.session_state.df.columns)]
    fill_technique = replace_nulls_form.selectbox("Choose technique", ["Mean", "Median"])
    if replace_nulls_form.form_submit_button("Replace !"):
        if fill_technique == "Mean":
            for col in [x[0] for x in cols_to_fill if x[1]]:
                st.session_state.df[col].fillna(st.session_state.df[col].mean(), inplace=True)
        elif fill_technique == "Median":
            for col in [x[0] for x in cols_to_fill if x[1]]:
                st.session_state.df[col].fillna(st.session_state.df[col].median(), inplace=True)
        st.rerun()

    st.header("Remove duplicated")
    if st.button("Remove !"):
        st.session_state.df.drop_duplicates(inplace=True)
    
    st.header("Remove outliers")
    remove_outliers_form = st.form("remove outliers form")
    remove_outliers_cols = [[col, remove_outliers_form.checkbox(col, key=f"remove outliers{i}")] for i, col in enumerate(st.session_state.df.select_dtypes('number'))]
    if remove_outliers_form.form_submit_button("Remove outliers !"):
        for col in remove_outliers_cols:
            if col[1] == False:
                continue
            Q1 = st.session_state.df[col[0]].quantile(.25)
            Q3 = st.session_state.df[col[0]].quantile(.75)
            IQR = Q3 - Q1
            lower_fence = Q1 - 1.5 * IQR
            upper_fence = Q3 + 1.5 * IQR
            st.session_state.df.loc[st.session_state.df[col[0]] < lower_fence, col[0]] = lower_fence
            st.session_state.df.loc[st.session_state.df[col[0]] > upper_fence, col[0]] = upper_fence
        st.rerun()

    st.header("One-hot encoding")
    one_hot_encoding_form = st.form("one hot encoding")
    one_hot_encoding_cols = [[col, one_hot_encoding_form.checkbox(col, key=f"one hot encoding{i}")] for i, col in enumerate(st.session_state.df.select_dtypes('category'))]
    one_hot_encoding_form.markdown("---")
    remove_first_column = one_hot_encoding_form.checkbox("Remove first column")
    if one_hot_encoding_form.form_submit_button("Encode !"):
        st.session_state.df = pd.get_dummies(st.session_state.df, columns=[col[0] for col in one_hot_encoding_cols if col[1]], drop_first=remove_first_column)
        st.rerun()

    st.header("Information & Statistics")
    if st.button("Show !", key='info'):
        st.text("Columns number: " + str(st.session_state.df.shape[1]))
        st.text("Records number: " + str(st.session_state.df.shape[0]))
        st.text("Dublicates number: " + str(st.session_state.df.duplicated().sum()))
        null_values = st.session_state.df.isnull().sum()
        st.table(pd.DataFrame({
            "type": st.session_state.df.dtypes,
            "nulls": null_values,
            "nulls (%)": null_values * 100 / st.session_state.df.shape[0],
            "unique": st.session_state.df.select_dtypes(exclude='number').nunique(),
            "min": st.session_state.df.select_dtypes(include='number').min(),
            "max": st.session_state.df.select_dtypes(include='number').max()
        }))

    st.header("Bar plot (Numerical/Categorical)")
    bar_plot_form = st.form("bar plot")
    bar_plot_y_axis = bar_plot_form.selectbox("Select number:", [col for col in st.session_state.df.select_dtypes('number').columns], key="bar plot y")
    bar_plot_x_axis = bar_plot_form.selectbox("Select category:", [col for col in st.session_state.df.select_dtypes('category').columns], key="bar plot x")
    count_plot_hue = bar_plot_form.radio("Choose hue column:", ['None']+[col for col in st.session_state.df.select_dtypes(exclude='number')])
    if bar_plot_form.form_submit_button("Plot !"):
        fig, ax = plt.subplots()
        sns.barplot(x=bar_plot_x_axis, y=bar_plot_y_axis, data=st.session_state.df, hue=None if count_plot_hue == 'None' else count_plot_hue,palette='bright', ax=ax)
        st.pyplot(fig)

    st.header("Scatter plot (Numerical/Numerical)")
    scatter_plot_form = st.form("scatter plot")
    scatter_plot_y_axis = scatter_plot_form.selectbox("Select number:", [col for col in st.session_state.df.select_dtypes('number').columns], key="scatter plot y")
    scatter_plot_x_axis = scatter_plot_form.selectbox("Select number:", [col for col in st.session_state.df.select_dtypes('number').columns], key="scatter plot x")
    count_plot_hue = scatter_plot_form.radio("Choose hue column:", ['None']+[col for col in st.session_state.df.select_dtypes(exclude='number')])
    if scatter_plot_form.form_submit_button("Plot !"):
        fig, ax = plt.subplots()
        sns.scatterplot(x=scatter_plot_x_axis, y=scatter_plot_y_axis, data=st.session_state.df, hue=None if count_plot_hue == 'None' else count_plot_hue, palette='bright', ax=ax)
        st.pyplot(fig)

    st.header("Heatmap plot (Categorical/Categorical)")
    heatmap_plot_form = st.form("heatmap plot")
    heatmap_plot_y_axis = heatmap_plot_form.selectbox("Select category:", [col for col in st.session_state.df.select_dtypes('category').columns], key="heatmap plot y")
    heatmap_plot_x_axis = heatmap_plot_form.selectbox("Select category:", [col for col in st.session_state.df.select_dtypes('category').columns], key="heatmap plot x")
    count_plot_hue = heatmap_plot_form.radio("Choose values column:", [col for col in st.session_state.df])
    if heatmap_plot_form.form_submit_button("Plot !"):
        if heatmap_plot_y_axis == count_plot_hue or heatmap_plot_x_axis == count_plot_hue:
            heatmap_plot_form.error('values column must not be in the selected categories')
        else:
            fig, ax = plt.subplots()
            agg = st.session_state.df.pivot_table(index=heatmap_plot_y_axis, columns=heatmap_plot_x_axis, aggfunc=len, values=count_plot_hue)
            sns.heatmap(data=agg, cmap='icefire', ax=ax)
            st.pyplot(fig)
    
    st.header("Heatmap")
    if st.button("Plot !", key="heatmap"):
        fig = plt.figure()
        sns.heatmap(data=st.session_state.df.select_dtypes('number').corr(), cmap='icefire', annot=True)
        st.pyplot(fig)
    
    st.header("Pair plot")
    hue = st.radio("Choose hue column: ", st.session_state.df.columns)
    if st.button("Plot !", key="pairplot"):
        fig = sns.pairplot(st.session_state.df[st.session_state.df.columns], hue=hue, palette='bright')
        st.pyplot(fig)

    st.header("Box plot")
    box_plot_form = st.form("box plot form")
    box_plot_cols = [[col, box_plot_form.checkbox(col, key=f"box plot{i}")] for i, col in enumerate(st.session_state.df.select_dtypes('number'))]
    if box_plot_form.form_submit_button("Plot !"):
        for col in box_plot_cols:
            if col[1] == False:
                continue
            fig, ax = plt.subplots()
            ax.boxplot(st.session_state.df[col[0]], vert=False)
            ax.set_title(f"{col[0]} Box plot")
            ax.set_yticklabels([col[0]])
            ax.set_ylim(.5, 1.5)
            fig.tight_layout()
            st.pyplot(fig)

    st.header("Count plot")
    count_plot_form = st.form("count plot form")
    count_plot_hue = count_plot_form.radio("Choose hue column:", ['None']+[col for col in st.session_state.df.select_dtypes(exclude='number')])
    count_plot_col = count_plot_form.selectbox("Choose column to plot:", [col for col in st.session_state.df.select_dtypes(exclude='number')])
    if count_plot_form.form_submit_button("count plot !"):
        fig, ax = plt.subplots()
        sns.countplot(x=count_plot_col, data=st.session_state.df, palette='bright', ax=ax, hue=None if count_plot_hue == 'None' else count_plot_hue)
        st.pyplot(fig)

    st.header("Download new CSV file")
    file_name = st.text_input("File name", "new_csv")
    if st.button("Download File"):
        st.session_state.df.to_csv(file_name+".csv", index=False)