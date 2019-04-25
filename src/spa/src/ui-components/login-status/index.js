import { Component } from 'inferno';
import styles from './styles.module.scss';
import { AppState, Events } from '../../app-state'

export default class LoginStatus extends Component {
    constructor(props) {
        super(props);
        AppState.subscribe(this, Events.LOGIN, Events.LOGOUT);
        this.state = {
            user: null
        }
    }

    onAppEventLogin(event, data) {
        this.setState({ user: data });
    }
    
    onAppEventLogout(event, data) {
        this.setState({ user: null });
    }

    render() {
        return (
            <div>
                {this.state.user == null ? 'You are not logged in' : `Hello, ${this.state.user.name}`  }
            </div>
        )
    }
}