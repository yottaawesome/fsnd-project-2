import { render, Component } from 'inferno';
import styles from './styles.module.scss'
import autobind from 'auto-bind';

const githubClientId = document.querySelector("meta[name='github-client-id']").getAttribute("content");

export default class Login extends Component {
    constructor(props) {
        super(props);
        autobind(this);
    }

    render() {
        return (
            <div className={styles.red}>
                <h2>Login</h2>
                <a href={`https://github.com/login/oauth/authorize?scope=read:user%20user:email&client_id=${githubClientId}`}>Click here</a> to begin!
            </div>
        );
    }
}
