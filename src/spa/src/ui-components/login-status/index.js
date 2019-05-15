import autobind from 'auto-bind';
import { Component, linkEvent } from 'inferno';
import { GlobalState, Events, State } from '../../app-state';
import ServerApi from '../../api';
import styles from './styles.module.scss';

export default class LoginStatus extends Component {
  constructor(props) {
    super(props);
    autobind(this);
    GlobalState.subscribe(this, Events.LOGIN, Events.LOGOUT);
    this.state = {
      user: null
    }
  }

  componentWillUnmount() { 
    GlobalState.unsubscribe(this);
  }

  onAppEventLogin(event, data) {
    this.setState({ user: data });
  }
  
  onAppEventLogout(event, data) {
    this.setState({ user: null });
  }

  onLogoutClick() {
    ServerApi
      .logout()
      .then((response) => {
        GlobalState.setStateData(State.CURRENT_USER, null);
        GlobalState.raiseEvent(Events.LOGOUT, null);
        return response;
      });
  }

  render() {
    if(this.state.user == null)
      return (<div><a href="#login">Please log in</a></div>);

    // We need the no-policy due to Google APIs randomly spitting out 403s from localhost: https://stackoverflow.com/questions/30851685/google-drive-thumbnails-getting-403-rate-limit-exceeded
    return (
      <div>
        <img height="30" referrerPolicy="no-referrer" width="30" src={this.state.user.picture} alt="avatar" />
        { `Hello, ${this.state.user.name}!` } Not you? <button class="link-button" onClick={linkEvent(this, this.onLogoutClick)}>Logout</button>
      </div>
    );
  }
}