'use client';

import {
  Tabs,
  Tab,
  TabList,
  TabPanels,
  TabPanel,
  Grid,
  Column,
} from '@carbon/react';
import Image from 'next/image';
import React, { useState, useEffect } from 'react';
import ExportButton from './export.js';
import Articles from './articles.js';

export default function LandingPage() {
  const [today, setToday] = useState([]);
  const [articleData, setArticleData] = useState([])

  useEffect(() => {
    fetch('http://127.0.0.1:5000/today')
      .then((response) => response.json())
      .then((json) => setToday(json))
      .catch((error) => console.error(error));
  }, []);

    
  useEffect(() => {
    fetch('http://127.0.0.1:5000/all')
        .then((response) => response.json())
        .then((json) => setArticleData(json))
        .catch((e) => console.log(e))}, []);
  

  return (
    <Grid className="landing-page" fullWidth>
      <Column lg={16} md={8} sm={4} className="landing-page__banner">
        <h1 className="landing-page__heading">
          News Analysis with watson<span class="x_char">x</span>
        </h1>
      </Column>
      <Column lg={16} md={8} sm={4} className="landing-page__r2">
        <Tabs defaultSelectedIndex={0}>
          <TabList className="tabs-group" aria-label="Page navigation">
            <Tab>Today's News</Tab>
            <Tab>Articles</Tab>
            <Tab>Export</Tab>
          </TabList>
          <TabPanels>
            <TabPanel>
              <Grid className="tabs-group-content">
                <Column
                  md={4}
                  lg={7}
                  sm={4}
                  className="landing-page__tab-content"
                >
                  {today.map((element) => (
                    <>
                      <h3 className="landing-page__subheading">
                        {element.category}
                      </h3>
                      {element.summaries.map((summ) => (
                        <p className="landing-page__p">{summ}</p>
                      ))}
                    </>
                  ))}
                </Column>
                <Column md={4} lg={{ span: 8, offset: 8 }} sm={4}>
                  <Image
                    className="landing-page__illo"
                    src="/tab-illo.png"
                    alt="Carbon illustration"
                    width={604}
                    height={498}
                  />
                </Column>
              </Grid>
            </TabPanel>
            <TabPanel>
              <Grid className="tabs-group-content">
                <Column
                  lg={16}
                  md={8}
                  sm={4}
                  className="landing-page__tab-content"
                >
                  <Articles articleData={articleData}/> 
                  
                </Column>
              </Grid>
            </TabPanel>
            <TabPanel>
              <Grid className="tabs-group-content">
                <Column
                  lg={16}
                  md={8}
                  sm={4}
                  className="landing-page__tab-content"
                >
                  <ExportButton articleData={articleData}/>
                </Column>
              </Grid>
            </TabPanel>
          </TabPanels>
        </Tabs>
      </Column>
    </Grid>
  );
}
