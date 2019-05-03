import { Component, linkEvent } from 'inferno';
import autobind from 'auto-bind';
import ServerApi from '../../api';
import { GlobalState, State, Events } from '../../app-state';
import styles from './styles.module.scss'

const githubClientId = document.querySelector("meta[name='github-client-id']").getAttribute("content");
const googleClientId = document.querySelector("meta[name='google-client-id']").getAttribute("content");
const pageState = document.querySelector("meta[name='page-state']").getAttribute("content");

/*function start() {
    console.log('load')
    gapi.load('auth2', function() {
        auth2 = gapi.auth2.init({
            client_id: googleClientId,
            // Scopes to request in addition to 'profile' and 'email'
            //scope: 'additional_scope'
        });
    });
}*/

export default class Login extends Component {
    constructor(props) {
        super(props);
        autobind(this);
    }

    onGoogleLoginClick() {
        auth2.grantOfflineAccess().then(this.signInCallback);
    }

    componentDidMount() {
    }

    signInCallback(authResult) {
        if (!authResult['code']) {
            console.error('An error occurred and no code was given.');
            return;
        }

        ServerApi
            .postGoogleAuthCode(pageState, authResult['code'])
            .then(response => {
                if(response.status == 401)
                    return Promise.reject("Failed to authenticate");
                return response.json();
            })
            .then(json => {
                GlobalState.setStateData(State.CURRENT_USER, json);
                GlobalState.raiseEvent(Events.LOGIN, json);
                window.location.hash = '#/';
                return json;
            })
            .catch(err => console.error(`Google login error: ${err}`))
    }

    render() {
        return (
            <div className={styles.red}>
                <h2>Login</h2>

                <p><a href={`https://github.com/login/oauth/authorize?scope=read:user%20user:email&client_id=${githubClientId}`}>Login with GitHub!</a></p>
                <p><button id="signinButton" onClick={ linkEvent(this, this.onGoogleLoginClick) }>Sign in with Google!</button></p>
                { /*<script onLoad={start} src="https://apis.google.com/js/client:platform.js" async defer></script>*/ }
            </div>
        );
    }
}
