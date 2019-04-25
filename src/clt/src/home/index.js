import { render, Component } from 'inferno';
import styles from './styles.module.scss'

export default class Home extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className={styles.red}>
                <h1 className={styles.red}>Hello</h1>
            </div>
        );
    }
}
