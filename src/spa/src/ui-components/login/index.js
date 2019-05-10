import { Component, linkEvent } from 'inferno';
import autobind from 'auto-bind';
import ServerApi from '../../api';
import { GlobalState, State, Events } from '../../app-state';
import styles from './styles.module.scss'
import githubIcon from './github-icon.svg';
import googleIcon from './google-icon.svg';

const githubClientId = document.querySelector("meta[name='github-client-id']").getAttribute("content");
const googleClientId = document.querySelector("meta[name='google-client-id']").getAttribute("content");
const pageState = document.querySelector("meta[name='page-state']").getAttribute("content");

let auth2 = null;

export default class Login extends Component {
  constructor(props) {
    super(props);
    autobind(this);
    this.state = { loadGScript: auth2 == null }
  }

  onGoogleLoginClick() {
    auth2.grantOfflineAccess().then(this.signInCallback);
  }

  loadGoogleApi() {
    let _this = this;
    gapi.load('auth2', function() {
      auth2 = gapi.auth2.init({
        client_id: googleClientId,
        // Scopes to request in addition to 'profile' and 'email'
        //scope: 'additional_scope'
      });
      _this.setState({ loadGScript: auth2 == null });
    });
  }

  signInCallback(authResult) {
    if (!authResult['code']) {
      console.error('An error occurred and no code was given.');
      return;
    }

    // We can't have this aas const as the redirect results in it being regenerated
    ServerApi
      .postGoogleAuthCode(pageState, authResult['code'])
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
      <div className={styles.root}>
        <h2>Please select how you want to log in</h2>
        <div className={styles.row}>
          <div className={styles.column}>
            <a href={`https://github.com/login/oauth/authorize?scope=read:user%20user:email&client_id=${githubClientId}`}>
              <img title="Sign in with GitHub" width="300" height="300" src={githubIcon} alt="GitHub logo" />
            </a>
          </div>
          <div className={styles.column}>
            <a href="javascript:" id="signinButton" onClick={ linkEvent(this, this.onGoogleLoginClick) }>
              <img title="Sign in with Google" width="300" height="300" src={googleIcon} alt="GitHub logo" />
            </a>
          </div>
        </div>

        {
          this.state.loadGScript 
            ? <script onLoad={linkEvent(this, this.loadGoogleApi)} src="https://apis.google.com/js/client:platform.js" async defer></script> 
            : null
        }
      </div>
    );
  }
}
