import React, { useState, useEffect, useReducer } from "react";
// nodejs library that concatenates classes
import classNames from "classnames";
// react components for routing our app without refresh
import { Link } from "react-router-dom";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
// @material-ui/icons
// core components
import Header from "components/Header/Header.js";
import Footer from "components/Footer/Footer.js";
import GridContainer from "components/Grid/GridContainer.js";
import GridItem from "components/Grid/GridItem.js";
import Button from "components/CustomButtons/Button.js";
// sections for this page
import HeaderLinks from "components/Header/HeaderLinks.js";

import styles from "assets/jss/material-kit-react/views/components.js";
import ReactMapGL, { Marker } from "react-map-gl";
import evStation from "assets/img/logo.png";
import stationIMG from "assets/img/evStation.png";
import axiosInstance from "../../axiosApi"
import Dialog from '@material-ui/core/Dialog';
import Card from "components/Bill/Card.js";
import CardHeader from "components/Bill/CardHeader.js";

import CloseIcon from '@material-ui/icons/Close';
import { IconButton } from '@material-ui/core';
import CircularProgress from '@material-ui/core/CircularProgress';

import InfoIcon from '@material-ui/icons/Info';
import EvStation from '@material-ui/icons/EvStation';

// core components
import NavPills from "components/NavPills/NavPills.js";
import styles3 from "assets/jss/material-kit-react/views/componentsSections/pillsStyle.js";
import { ContactSupportOutlined } from "@material-ui/icons";

const useStyles = makeStyles(styles);
const useStyles2 = makeStyles(theme => ({
  paper: {
    overflowY: 'unset',
  },
  customizedButton: {
    position: 'absolute',
    left: '90%',
    top: '2%',
    backgroundColor: 'white',
    color: 'gray',
  }
}));
const useStyles3 = makeStyles(styles3)

export default function Map (props) {
  const classes = useStyles();
  const classes2 = useStyles2();
  const classes3 = useStyles3();
  const { ...rest } = props;
  const [viewPort, setViewPort] = useState ({
    latitude: 37.996904137698095,
    longitude: 23.731642389218965,
    width: "100vw",
    height: "100vh",
    zoom: 12
  });
  const navImageClasses = classNames(classes.imgRounded, classes.imgGallery);
  const [selectedStation, setSelectedStation] = useState(null);
  const [isLoading, setIsLoading] = useState(false)
  const [showPopUp, setShowPopUp] = useState(false);
  const [showPay, setShowPay] = useState(false);
  const [startCharge, setStartCharge] = useState(true)
  const [startDate, setStartDate] = useState()
  const [finishDate, setfinishDate] = useState()
  const [finishCharge, setFinishCharge] = useState(false)
  const [chargingTypeSelected, setChargingTypeSelected] = useState({
    AC: {
      selected: false,
      color: ""
    },
    DC: {
      selected: false,
      color: ""
    }
  });
  const [payMethod, setPayMethod] = useState(
    {
      cash: {
        selected: false,
        color: ""
      },
      credit: {
        selected: false,
        color: ""
      }
    }
  );


  const [stations, setStations] = useState([]);

  React.useLayoutEffect ( () => {
   const response = axiosInstance.get("stations/")
   .then (res => {
    let tempStationList = []
     for (let i = 0; i < res.data.length; i++) {
       let tempStation = {}
       tempStation.latitude = res.data[i].addressInfo.latitude;
       tempStation.longitude = res.data[i].addressInfo.longtitude;
       tempStation.id = res.data[i].id;
       tempStation.port = res.data[i].comments[0].ports[0].title;
       tempStation.operators = res.data[i].comments.length;
       tempStation.providerName = res.data[i].providers[0].name;
       tempStation.providerCostPerKWh = res.data[i].providers[0].costPerkWh;
       tempStation.usageCost = res.data[i].usageCost;
       tempStation.address = res.data[i].addressInfo.addressLine;
       tempStation.phone = res.data[i].addressInfo.contact_telephone;
       tempStation.title = res.data[i].addressInfo.title;
       tempStation.town = res.data[i].addressInfo.town;
       tempStation.pointID = res.data[i].comments[0].id;
       tempStation.providerID = res.data[i].providers[0].id;
       tempStation.portID = res.data[i].comments[0].ports[0].id;
       tempStationList.push(tempStation)
     }
     setStations(tempStationList)
   })
   .catch (error => {
     console.log(error)
   })
  }, []);

  function handlePay () {
    setShowPay(true)
  }
  function handleNewSession () {
    let timeNow = new Date().toISOString()
    let finishdate = timeNow.slice(0,10) + " " + timeNow.slice(11,19) + ".00+00:00"
    let pay;
    if (payMethod.cash.selected) {
      pay = "Cash";
    }
    else  {
      pay = "Credit";
    }
    console.log(startDate);
    console.log(finishdate);

    const response = axiosInstance.post("user/mycars/chargingsession/", {
      ProviderID: selectedStation.providerID,
      StationID: selectedStation.id,
      PortID: selectedStation.portID,
      PointID: selectedStation.pointID,
      VehicleID: localStorage.getItem("selectedCar").toString(),
      kWh: true,
      accharger: chargingTypeSelected.AC.selected,
      kWhDelivered: 42,
      amount: null,
      connectionTime: startDate,
      disconnectTime: startDate,
      doneChargingTime: finishdate,
      payment:  pay
    })
    .then (res => {
      console.log(res)
    })
    .catch (error => {
      console.log(error.response);
    })
  }
  function Timer () {
    const timer = setTimeout(() => {
      setIsLoading(false)

    }, 3000);
    return (null);
  }
  return (
    <div>
      { isLoading &&     
        <Dialog open = { true } PaperProps={{
          style: {
            backgroundColor: 'transparent',
            boxShadow: 'none',
          },
        }}>
          <CircularProgress style = {{color: "#67ad5b"}} />
          <Timer></Timer>
        </Dialog>  
        }
      <Header
        brand="eevie"
        rightLinks={<HeaderLinks />}
        fixed
        color="white"
        
        {...rest}
      />
 

      <div className={classNames(classes.main)}>
        <div style={{ width: "100vw", height: "100vh" }}>
            <ReactMapGL
            {...viewPort}
            mapboxApiAccessToken={"pk.eyJ1Ijoic2hlZXJvIiwiYSI6ImNrbTFpcDVkbzJ4YjIycHAzaTJvbWtyOXYifQ.kjOwXg39LGtrcvUyJcqdSQ"}
            mapStyle= "mapbox://styles/mapbox/dark-v10"
            onViewportChange={viewPort => {
            setViewPort(viewPort);
            }}
            >
           { 
            stations.map((prop, key) => {
              if (prop === null) {
                return null
              }
               return (
                <Marker
                  key={ key }
                  latitude={ parseFloat(prop.latitude) }
                  longitude={  parseFloat(prop.longitude) }
               >
              <button
                style = { { backgroundColor: "transparent", border: "none" } }
                className="marker-btn"
                onClick={e => {
                  e.preventDefault();
                  setSelectedStation(prop);
                  setShowPopUp(true);
                }}
              >
                <img
                  alt="..."
                 src={evStation}
                 className={navImageClasses}
                    />
              </button>
           </Marker>
              ); 
            })
           }
        { showPay &&     
        <Dialog 
          open = { showPopUp } 
          PaperProps={{
            style: {
               boxShadow: 'none',
               width: "100%",
               height: "70%",
            
            },
          }}
          >
          <IconButton className={classes2.customizedButton} onClick = {() => {
            setShowPay(false)
            }}>
            <CloseIcon/>
          </IconButton>
          <GridContainer style = {{padding:35}} justify = "center">
          {startCharge && 
          <React.Fragment>
          <GridItem xs={12} sm={12} md={6} lg={6}>
              <Card>
                <CardHeader>
                  <GridContainer justify = "center">
                  <b style = {{userSelected: "none"}}> Type</b> 
                    <GridItem>
                      <p>
                        { }
                      </p>
                    </GridItem>
                  </GridContainer>
                  <GridContainer justify = "center">
                    <Button size = {"lg"} color = { chargingTypeSelected.AC.color } onClick = {() => {
                      setChargingTypeSelected({
                        AC: {
                          selected: true,
                          color: "success"
                        },
                        DC: {
                          selected: false,
                          color: ""
                        }
                      })
                    }}>AC</Button>
                    <Button size = {"lg"} color = { chargingTypeSelected.DC.color} onClick = {() => {
                      setChargingTypeSelected({
                        AC: {
                          selected: false,
                          color: ""
                        },
                        DC: {
                          selected: true,
                          color: "success"
                        }
                      })
                    }}>DC</Button>
                  </GridContainer>
                </CardHeader>
              </Card>
            </GridItem>
            <GridItem xs={12} sm={12} md={6} lg={6}>
              <Card>
                <CardHeader>
                  <GridContainer justify = "center" style = {{userSelected: "none"}}>
                    <b>Pay Method</b>
                    <GridItem>
                      <p>
                        { }
                      </p>
                    </GridItem>
                  </GridContainer>
                  <GridContainer justify = "center">
                    <Button size = {"lg"} color = { payMethod.cash.color } onClick = {() => {
                      setPayMethod({
                        cash: {
                          selected: true,
                          color: "success"
                        },
                        credit: {
                          selected: false,
                          color: ""
                        }
                      })
                    }}>Cash</Button>
                    <Button size = {"lg"} color = { payMethod.credit.color} onClick = {() => {
                      setPayMethod({
                        cash: {
                          selected: false,
                          color: ""
                        },
                        credit: {
                          selected: true,
                          color: "success"
                        }
                      })
                    }}>Credit</Button>
                  </GridContainer>
                </CardHeader>
              </Card>
            </GridItem> 
            </React.Fragment>
            }  
            {startCharge && 
              <React.Fragment>
              <GridItem xs={12} sm={12} md={12} lg={12} style = {{padding: 15}}>
                <GridContainer justify = "center">
                <img
                  alt="..."
                 src={stationIMG}
                 className={navImageClasses}
                 style = {{userSelected: "none"}}
                    />
                </GridContainer>
              </GridItem>
            </React.Fragment>

            }
            {finishCharge && 
              <React.Fragment>
                 <GridItem xs={12} sm={12} md={6} lg={6}>
              <Card>
                <CardHeader>
                  <GridContainer justify = "center">
                    <b style = {{userSelected: "none"}}> Type</b> 
                    <GridItem>
                      <p>
                        { }
                      </p>
                    </GridItem>
                  </GridContainer>
                  <GridContainer justify = "center">
                    <Button size = {"lg"} color = { chargingTypeSelected.AC.color }>AC</Button>
                    <Button size = {"lg"} color = { chargingTypeSelected.DC.color}>DC</Button>
                  </GridContainer>
                </CardHeader>
              </Card>
            </GridItem>
            <GridItem xs={12} sm={12} md={6} lg={6}>
              <Card>
                <CardHeader>
                  <GridContainer justify = "center" style = {{userSelected: "none"}}>
                    <b>Pay Method</b>
                    <GridItem>
                      <p>
                        { }
                      </p>
                    </GridItem>
                  </GridContainer>
                  <GridContainer justify = "center">
                    <Button size = {"lg"} color = { payMethod.cash.color }>Cash</Button>
                    <Button size = {"lg"} color = { payMethod.credit.color}>Credit</Button>
                  </GridContainer>
                </CardHeader>
              </Card>
            </GridItem>
                <GridItem xs={12} sm={12} md={12} lg={12} style = {{padding: 0}}>
                  <GridContainer justify = "center">
                    <h3>Charging in progress...</h3> 
                  </GridContainer>
                </GridItem>
                <GridItem xs={12} sm={12} md={12} lg={12} style = {{padding: 33}}>
                  <GridContainer justify = "center">
                  <CircularProgress style = {{color: "black"}} />  
                  </GridContainer>
                </GridItem>
              </React.Fragment>
            }
            <GridItem xs={12} sm={12} md={3} lg={3}>
              <GridContainer justify = "center">
                {startCharge && <Button color = {"success"}size = {"lg"}fullWidth = {true} onClick = {() => {
                  var isoDateString = new Date().toISOString();
                  console.log(isoDateString.slice(0,10) + " " + isoDateString.slice(11,19) + ".00+00:00")
                  setStartDate(isoDateString.slice(0,10) + " " + isoDateString.slice(11,19) + ".00+00:00");
                  if ((payMethod.cash.selected || payMethod.credit.selected) && (chargingTypeSelected.AC.selected || chargingTypeSelected.DC.selected)) {
                    setStartCharge(false); setFinishCharge(true)
                  }
                }}>Start Charging</Button>}
                {finishCharge && <Button color = {"danger"}size = {"lg"}fullWidth = {true} onClick = {() => {
                  setFinishCharge(false); 
                  setStartCharge(true); 
                  setShowPay(false); 
                  setShowPopUp(false);
                  handleNewSession();
                  //setIsLoading(true);
                  }}>End Session</Button>}
              </GridContainer>
            </GridItem>
          </GridContainer>
         
        </Dialog>  
        }
        { showPopUp &&     
        <Dialog 
          onClose = {
            () => {
              setShowPay(false)
              setShowPopUp(false)
            }
          }
          open = { showPopUp } 
          PaperProps={{
            style: {
               boxShadow: 'none',
               width: "100%",
               height: "70%",
            
            },
          }}
          >
          <IconButton className={classes2.customizedButton} onClick = {() => {setShowPopUp(false)}}>
            <CloseIcon/>
          </IconButton>

          <GridContainer style = {{padding: 20}} justify = "center">
          <h2 style = { {color: "#67ad5b"} }> {selectedStation.title.slice(0,29)} </h2>
            <GridItem xs={12} sm={12} md={12} lg={12}>
              <NavPills
                color="success"
                horizontal={{
                  tabsGrid: { xs: 12, sm: 4, md: 4 },
                  contentGrid: { xs: 12, sm: 8, md: 8 }
                }}
                tabs={[
                  {
                    tabButton: "New Session",
                    tabIcon: EvStation,
                    tabContent: (
                      <span>
                        <p>
                          Station ID: <b> {selectedStation.id}</b>
                        </p>
                        <p>
                          Port: <b> {selectedStation.port} </b>
                        </p>
                        <p>
                          Address: <b> {selectedStation.address} </b>
                        </p>
                        <p>
                          Town: <b> {selectedStation.town} </b>
                        </p>
                        <p>
                          Aviable: <b>{selectedStation.operators}</b>
                        </p>
                        <p>
                          Rating: <b style = {{color: "#67ad5b"}}>4.9</b> (102)
                        </p>
                        <br />
                        <p>
                        </p>
                      </span>
                    )
                  },
                  {
                    tabButton: "Station Info",
                    tabIcon: InfoIcon,
                    tabContent: (
                      <span>
                        <p>
                          Provider: <b>{selectedStation.providerName}</b>
                        </p>
                        <p>
                          Cost Per KWh: <b>0.153</b>
                        </p>
                        <p>
                          Usage Cost: <b> {selectedStation.usageCost} </b>
                        </p>
                        <br></br>
                        <p>
                          <b>Contact Info</b>
                        </p>
                        <p>
                          Telephone: <b>{selectedStation.phone}</b>
                        </p>
                      </span>
                    )
                  }
                ]}
              />
            </GridItem>
            <GridItem>
              <br></br>
            </GridItem>
            <GridItem>
              <Button fullWidth = {true }color = "success" onClick = {() => {handlePay();}}>
                New Session
              </Button>
            </GridItem>
          </GridContainer>
         
        </Dialog>  
        }
           </ReactMapGL>
        </div>
      </div>
      <Footer />
    </div>
  );
}
