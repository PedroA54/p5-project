import React from "react";
import Login from '../components/User/Login';
import { NavLink } from "react-router-dom";



function EntryPage() {
    return (
        <>
            <h1 className="title-login"> Recipe Realm</h1>
            
            <section>
                <Login />
            </section>
            
            <div className="log-in-link">
                <span>Not a member yet?</span>
                <NavLink to="/signup">
                    Sign Up
                </NavLink>
            </div>
        </>
    );
}

export default EntryPage;
