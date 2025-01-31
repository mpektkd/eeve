import React from "react";
import { Redirect } from "react-router";
// nodejs library that concatenates classes
import classNames from "classnames";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
// @material-ui/icons
import AttachMoneyIcon from '@material-ui/icons/AttachMoney';
import EqualizerIcon from '@material-ui/icons/Equalizer';
import DriveEtaIcon from '@material-ui/icons/DriveEta';
// core components
import Header from "components/Header/Header.js";
import Footer from "components/Footer/Footer.js";
import Button from "components/CustomButtons/Button.js";
import GridContainer from "components/Grid/GridContainer.js";
import GridItem from "components/Grid/GridItem.js";
import HeaderLinks from "components/Header/HeaderLinks.js";
import NavPills from "components/NavPills/NavPills.js";
import Parallax from "components/Parallax/Parallax.js";
import CircularProgress from '@material-ui/core/CircularProgress';

import profile from "assets/img/faces/christian.jpg";
import Dialog from '@material-ui/core/Dialog';

import Card from "components/Bill/Card.js";
import CardHeader from "components/Bill/CardHeader.js";
import CardIcon from "components/Bill/CardIcon.js";
import CardBody from "components/Bill/CardBody.js";
import CardFooter from "components/Bill/CardFooter.js";
import styles from "assets/jss/material-kit-react/views/profilePage.js";
import DateRange from "@material-ui/icons/DateRange";
import Table from "components/Table/Table.js";
import axiosInstance from "../../axiosApi";
import CustomDropdown from "components/CustomDropdown/CustomDropdown.js";
import Car2 from '@material-ui/icons/DriveEta';

import styles2 from "assets/jss/material-dashboard-react/views/dashboardStyle.js";

const useStyles = makeStyles(styles);
const useStyles2 = makeStyles(styles2);

export default function ProfilePage(props) {
  const classes = useStyles();
  const classes2 = useStyles2();
 // const [billList, setBillList] = React.useState([])
  const [bilLList, setBilLList] = React.useState([])
  const [monthlyBillList, setMonthlyBillList] = React.useState([])
  const [monthlyBilLList, setMonthlyBilLList] = React.useState([])
  const [carSelected, setCarSelected] = React.useState(false)
 // const [itemSelected, setItemSelected] = React.useState(false)
  const [carList, setCarList] = React.useState([])
  const [carList2, setCarList2] = React.useState([])
  const [isLoading, setIsLoading] = React.useState(false)
  const [pageNeedsRender, setPageNeedsRender] = React.useState(true)
  const { ...rest } = props;
  const imageClasses = classNames(
    classes.imgRaised,
    classes.imgRoundedCircle,
    classes.imgFluid
  );
  const navImageClasses = classNames(classes.imgRounded, classes.imgGallery);
  React.useLayoutEffect ( () => {
    if (!pageNeedsRender) {
      return;
    }
    const response = axiosInstance.get('user/mycars/')
      .then(res => {
        let car = {}
        let tempCarList = [] 
        for (let i = 0; i < res.data.length; i++) {
          if (res.data[i].release_year)
            car.name = res.data[i].car.brandName + " " + res.data[i].car.model + " " + res.data[i].car.release_year
          else 
            car.name = res.data[i].car.brandName + " " + res.data[i].car.model
          car.id = res.data[i].id;
          tempCarList.push(car)
          car = {}
        }
  
       localStorage.setItem("selectedCar", tempCarList[0].id)
        
        setCarList(tempCarList);
      })
      .catch(error => {
        console.log(error)
      })
     const response2 = axiosInstance.get('user/mybills/')
      .then(res => {
        //let bill = {}
        //let tempBillList = []
        let tempBilLList = []
        for (let i = 0; i < res.data.length; i++) {
          let bilL = []
          /* if (!res.data[i].is_paid) {
            bill.amount = (res.data[i].total).toFixed(2);
            bill.date = res.data[i].date_created.toString().slice(0,10);
            bill.id = res.data[i].id;
            tempBillList.push(bill);
          } */
          bilL.push(res.data[i].id.toString());
          bilL.push(res.data[i].date_created.toString().slice(0,10));
          bilL.push("$"+(res.data[i].total.toFixed(2)).toString());
          if (res.data[i].is_paid) {
            bilL.push("paid off");
          }
          else {
            bilL.push("due");
          }
          tempBilLList.push(bilL);
         // bill = {}
        }
       // setBillList(tempBillList)
        setBilLList(tempBilLList);
        setPageNeedsRender(false)
      })
      .catch(error => {
        console.log(error)
      }) 
      const response3 = axiosInstance.get('user/mymonthbills/')
        .then(res => {
          console.log(res)
          let bill = {}
          let tempBillList = []
          let tempBilLList = []
        for (let i = 0; i < res.data.length; i++) {
          let bilL = []
          if (res.data[i].monthly_total > 0) {
            bill.amount = (res.data[i].monthly_total).toFixed(2);
            bill.date = res.data[i].start_date.toString().slice(0,10);
            bill.id = res.data[i].id;
            tempBillList.push(bill);
          }
          bilL.push(res.data[i].id.toString());
          bilL.push(res.data[i].start_date.toString().slice(0,10));
          if (res.data[i].monthly_total <= 0) {
            bilL.push("$"+((-res.data[i].monthly_total).toFixed(2)).toString());
            bilL.push("paid off");
          }
          else {
            bilL.push("$"+(res.data[i].monthly_total.toFixed(2)).toString());
            bilL.push("due");
          }
          tempBilLList.push(bilL)
          bill = {}
        }
        setMonthlyBillList(tempBillList);
        setMonthlyBilLList(tempBilLList)
      })
        .catch(error => {
          console.log(error)
        })
        const response4 = axiosInstance.get('cars/')
      .then(res => {
        console.log(res)
        let car = {}
        let tempCarList = []
        for (var i = 0; i <res.data.length; i++) {
          if (res.data[i].release_year)
            car.name = res.data[i].brandName + " " + res.data[i].model + " " + res.data[i].release_year
          else 
            car.name = res.data[i].brandName + " " + res.data[i].model

          car.id = res.data[i].id;
          tempCarList.push(car)
          car = {}
        }
        setCarList2(tempCarList);        
      })

  }, []);

  function pay (props) {
    setIsLoading(true)
    const response = axiosInstance.post("user/payoff/", {BillID: props.props.id})
      .then(res => {
        console.log(res)
      })
      .catch(error => {
        console.log(error)
      })
  }
  function Bill(props) {
    return (<GridItem xs={12} sm={7} md={4}>
      <Card>
        <CardHeader color="success" stats icon>
          <CardIcon color="success" onClick = {() => pay(props)}>
            Click to pay
          </CardIcon>
          <p className={classes2.cardCategory}>Bill</p>
          <h3 className={classes2.cardTitle}>${props.props.amount}</h3>
        </CardHeader>
        <CardFooter stats>
          <div className={classes2.stats}>
            <DateRange />
            {props.props.date}
          </div>
        </CardFooter>
      </Card>
    </GridItem>);
  }

  function monthPay (props) {
    setIsLoading(true)
     const response = axiosInstance.post("user/monthpayoff/", {BillID: props.props.id})
      .then(res => {
        console.log(res)
      })
      .catch(error => {
        console.log(error)
      }) 
  }

  function MonthlyBill(props) {
    return (<GridItem xs={12} sm={7} md={4}>
      <Card>
        <CardHeader color="success" stats icon>
          <CardIcon color="success" onClick = {() => monthPay(props)}>
            Click to pay
          </CardIcon>
          <p className={classes2.cardCategory}>Monthly Bill</p>
          <h3 className={classes2.cardTitle}>${props.props.amount}</h3>
        </CardHeader>
        <CardFooter stats>
          <div className={classes2.stats}>
            <DateRange />
            {props.props.date}
          </div>
        </CardFooter>
      </Card>
    </GridItem>);
  }

  
  function Car (props) {
    return (<GridItem xs={12} sm={7} md={4}>
      <Card>
        <CardHeader styles = {{userSelected: "none" }} color="success" stats icon>
         {
         (localStorage.getItem("selectedCar") === props.props.id.toString()) && <CardIcon color="success" onClick = {() => selectCar(props)}>
            Active Car
          </CardIcon>
          }
          {
          (localStorage.getItem("selectedCar") !== props.props.id.toString()) &&
           <CardIcon color="success" onClick = {() => selectCar(props)}>
            Select Car
          </CardIcon>
          }
          <p className={classes2.cardCategory}>vehicle</p>
          <h3 className={classes2.cardTitle}>{props.props.name.slice(0,18)}</h3>
        </CardHeader>
      </Card>
    </GridItem>);
  }
  function selectCar (prop) {
    localStorage.setItem("selectedCar", prop.props.id);
    setCarSelected(prop.props.id);
  }
  function Timer () {
    const timer = setTimeout(() => {
      setIsLoading(false)
      window.location.reload();

    }, 3000);
    return (null);
  }
 
  function handleInsertCar () {
    const response = axiosInstance.post("user/newcar/", {
      CarID: localStorage.getItem("carForSignUp")
    })
    .then (res => {
      console.log(res)
      setIsLoading(true)
    })
    .catch (error => {
      console.log(error)
    })
  }
     
  return (
    <div>
      { !localStorage.getItem("isLoggedIn") && <Redirect to = "/login-page"/>}
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
        color="transparent"
        brand="eevie"
        rightLinks={<HeaderLinks />}
        fixed
        changeColorOnScroll={{
          height: 200,
          color: "white"
        }}
        {...rest}
      />
      <Parallax small filter image={require("assets/img/mybgblur.jpg")} />
      <div className={classNames(classes.main, classes.mainRaised)}>
        <div>
          <div className={classes.container}>
            <GridContainer justify="center">
              <GridItem xs={12} sm={12} md={6}>
                <div className={classes.profile}>
                  <div>
                    <img src={profile} alt="..." className={imageClasses} />
                  </div>
                  <div className={classes.name}>
                    <h3 className={classes.title}> { localStorage.getItem("username") } </h3>
                  </div>
                </div>
              </GridItem>
            </GridContainer>
            <div className={classes.description}>
              <p>
               Personilised data{" "}
              </p>
            </div>
            <GridContainer justify="center">
              <GridItem xs={12} sm={12} md={9} className={classes.navWrapper}>
                <NavPills
                  alignCenter
                  color="success"
                  tabs={[
                    {
                      tabButton: "Monthly bills",
                      tabIcon: AttachMoneyIcon,
                      tabContent: (
                        <GridContainer style = { {padding: 20}} justify = "center">
                          {
                            monthlyBillList.map((prop, key ) => {
                              return (
                                <MonthlyBill key = {key} props = { prop }/>
                              );
                            })
                          }
                        </GridContainer>
                      )
                    },
                    /* {
                      tabButton: "Sessions",
                      tabIcon: AttachMoneyIcon,
                      tabContent: (
                        <GridContainer style = { {padding: 20}} justify = "center">
                          {
                            billList.map((prop, key ) => {
                              return (
                                <Bill key = {key} props = { prop }></Bill>
                              );
                            })
                          }
                        </GridContainer>
                      )
                    }, */
                    {
                      tabButton: "Statistics",
                      tabIcon: EqualizerIcon,
                      tabContent: (
                        <GridContainer justify="center">                       
                          <GridItem xs={12} sm={12} md={12}>
                            <Card>
                              <CardHeader color="success">
                                <h4 className={classes.cardTitleWhite}>Session History</h4>
                              </CardHeader>
                              <CardBody>
                                <Table
                                  tableHeaderColor="success"
                                  tableHead={["Bill ID", "Date", "Amount", "State"]}
                                  tableData={bilLList}
                                />
                              </CardBody>
                            </Card>
                          </GridItem>
                          <GridItem xs={12} sm={12} md={12}>
                            <Card>
                              <CardHeader color="success">
                                <h4 className={classes.cardTitleWhite}>Monthly Bill History</h4>
                              </CardHeader>
                              <CardBody>
                                <Table
                                  tableHeaderColor="success"
                                  tableHead={["Bill ID", "Date", "Amount", "State"]}
                                  tableData={monthlyBilLList}
                                />
                              </CardBody>
                            </Card>
                          </GridItem>
                        </GridContainer>
                      )
                    },
                    {
                      tabButton: "My vehicles",
                      tabIcon: DriveEtaIcon,
                      tabContent: (
                        <GridContainer style = { {padding: 20}}>
                          <GridItem>
                            <CustomDropdown
                                dropDownCar = { true }
                                buttonText="Select Car"
                                buttonProps={{
                                  color: "success"
                                }}
                                buttonIcon={ Car2 }
                                dropdownList={ carList2 }
                                />   
                          </GridItem>
                          <GridItem>
                            <Button color = "success" onClick = { handleInsertCar }>
                              Insert this Car!
                            </Button>
                            <GridItem>
                              <p>
                                { }
                              </p>
                            </GridItem>
                            <GridItem>
                              <p>
                                { }
                              </p>
                            </GridItem>
                            <GridItem>
                              <p>
                                { }
                              </p>
                            </GridItem>
                            <GridItem>
                              <p>
                                { }
                              </p>
                            </GridItem>
                            <GridItem>
                              <p>
                                { }
                              </p>
                            </GridItem>
                            <GridItem>
                              <p>
                                { }
                              </p>
                            </GridItem>
                            <GridItem>
                              <p>
                                { }
                              </p>
                            </GridItem>
                          </GridItem>   
                          {
                            carList.map((prop, key ) => {
                              return (
                                <Car key = {key} props = { prop }></Car>
                              );
                            })
                          }
                        </GridContainer>
                      )
                    }
                  ]}
                />
              </GridItem>
            </GridContainer>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
}
