import React, { useState, useRef, useEffect } from 'react'
import { Dropdown, Grid, Row, Column, ContainedList, ContainedListItem } from '@carbon/react'
import { CSVLink } from 'react-csv'

const Articles = ({articleData}) => {
    var sources = new Set()
    const [selectedSource, setSource] = useState('');
    const [selectedArticle, setArticle] = useState({});
    articleData.forEach((article) => {
        sources.add(article.Source)
    })

    let selectSource = (e) => {
        console.log(e)
        setSource(e.selectedItem)
    }

    let articleClicked = (e) => {
        console.log(e.target.innerText)
        //setArticle(e.target.innerText)
        setArticle(articleData.find((element) => element.Title.includes(e.target.innerText)))
        console.log(selectedArticle)
    }

  return (
    <>
        <h2 className="landing-page__middleheading"> Search By Article</h2>
        <Dropdown items={Array.from(sources)} onChange={selectSource} label='Select News Source'/>
        <Grid fullWidth className='articlesgrid'>
                <Column lg={4}>
                <ContainedList className='articleslist' isInset='true' kind='on-page' label={selectSource == '' ? '': (selectedSource + ' articles')}>
                    {articleData.map((article) => (
                        (article.Source == selectedSource) ? (<ContainedListItem onClick={articleClicked}>{article.Title}</ContainedListItem>) : <></>
                    ))}
                </ContainedList>
                </Column>
                <Column lg={12} className='articlestext'> {selectedArticle != null ? (<><h2>{selectedArticle.Title}</h2> <br/><p>{selectedArticle.Text}</p></>) : (<></>)}
                </Column>
        </Grid>
    </>
  )
}

export default Articles