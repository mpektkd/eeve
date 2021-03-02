import React from "react"
import { Router, Route, Switch } from "react-router-dom";
import { createBrowserHistory } from "history";

// pages for this product
import Home from "views/Home/Home.js";
import LandingPage from "views/LandingPage/LandingPage.js";
import ProfilePage from "views/ProfilePage/ProfilePage.js";
import LoginPage from "views/LoginPage/LoginPage.js";
import SignupPage from "views/SignupPage/SignupPage.js";
import Map from "views/Map/Map.js";

//Axios
import axiosInstance from "./axiosApi";

var hist = createBrowserHistory();

export default function App (props) {
    const [user, setUser] = React.useState("");
    const [loggedIn, setLoggedIn] = React.useState(null);
    React.useLayoutEffect ( () => {
        const response = axiosInstance.get('current_user/')
          .then(res => {
            setUser(res.data.username);
            localStorage.setItem("username", res.data.username);
            setLoggedIn(true)
            //localStorage.setItem("userIsLoggedIn", true);
          })
          .catch(error => {
            console.log(error)
          })
      });

    return (
        <Router history={hist}>
            <Switch>
            <Route path="/landing-page" component={LandingPage} />
            <Route path="/profile-page" component={ProfilePage} />
            <Route path="/login-page" component={LoginPage} />
            <Route path="/signup-page" component={SignupPage} />
            <Route path = "/map" component = {Map} />
            <Route path="/" component={ Home } />
            </Switch>
        </Router>
    );
} 