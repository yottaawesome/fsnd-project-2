import { render, Component } from 'inferno';
import styles from './styles.module.scss'

export default class Login extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className={styles.red}>
                <h1>Login</h1>
            </div>
        );
    }
}
