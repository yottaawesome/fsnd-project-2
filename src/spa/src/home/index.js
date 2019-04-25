import { render, Component } from 'inferno';
import { AppState, Events } from '../app-state'
import styles from './styles.module.scss'

export default class Home extends Component {
    constructor(props) {
        super(props);
        //this.componentDidMount = this.componentDidMount.bind(this);
        AppState.subscribe(this, Events.LOGIN);
    }

    componentDidMount() {
        console.log("Mount")
    }

    componentWillUnmount() {
        console.log("Unmount")
        AppState.unsubscribe(this);
    }

    onAppEventLogin(event, data) {
        console.log("Called")
    }

    render() {
        AppState.raiseEvent(Events.LOGIN, 1);
        return (
            <div className={styles.red}>
                <h1>Hello</h1>
            </div>
        );
    }
}
