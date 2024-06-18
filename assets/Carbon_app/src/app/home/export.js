import React, { useState, useRef, useEffect } from 'react'
import { Button } from '@carbon/react'
import { CSVLink } from 'react-csv'
import axios from 'axios'

const ExportButton = ({articleData}) => {

  const csvLink = useRef() // setup the ref that we'll use for the hidden CsvLink click once we've updated the data

  const downloadCSV = () => {
    console.log(articleData)
    csvLink.current.link.click()
  }

  return (
    <div>
      <Button onClick={downloadCSV}>Download articles to csv</Button>
      <CSVLink
         data={articleData}
         filename='articles.csv'
         className='hidden'
         ref={csvLink}
         target='_blank'
      />
    </div>
  )
}

export default ExportButton