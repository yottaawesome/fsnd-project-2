import { Component } from 'inferno';
import styles from './index.module.scss';
import LoginStatus from '../login-status';

export default class Header extends Component {
    constructor(props) { 
        super(props);
    }

    render() {
        return (
            <div className={styles.root}>
                <div className={styles.column1}><h1>Welcome to your Digital Bookshelf!</h1></div>
                <div className={styles.column2}><LoginStatus /></div>
            </div>
        )
    }
}
