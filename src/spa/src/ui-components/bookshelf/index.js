import { Component } from 'inferno';
import styles from './index.module.scss';
import autobind from 'auto-bind';

export default class Bookshelf extends Component {
    constructor(props) { 
        super(props);
        autobind(this);
    }

    render() {
        return (
            <div className={styles.root}>
            </div>
        )
    }
}
