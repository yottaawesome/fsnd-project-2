import { Component, linkEvent } from 'inferno';
import autobind from 'auto-bind';
import ServerApi from '../../api';
import { categories } from './shared';
import { GlobalState, Events, State } from '../../app-state';
import styles from './styles.module.scss';

const mode = {
  NEW: 'new',
  EDIT: 'edit'
};

export default class NewEditBook extends Component {
  constructor(props) {
    super(props);
    autobind(this);
    this.state = this.initialState();
    GlobalState.subscribe(this, Events.LOGIN, Events.LOGOUT);
  }

  //#region LIFECYCLE
  componentDidMount() {
    this.refresh();
  }

  componentWillUnmount() {
    GlobalState.unsubscribe(this);
  }

  // We need this to handle changing routes, because the same component is used
  // and not remounted, so we need to manually detect this and refresh.
  componentWillReceiveProps(newProps) {
    this.props = newProps;
    this.refresh();
  }

  // It doesn't appear componentWillReceiveProps() gets invoked if
  // shouldComponentUpdate() is not defined, so just add it.
  shouldComponentUpdate() {
    return true;
  }
  //#endregion

  //#region GLOBAL EVENTS
  onAppEventLogin(evt, data) {
    this.refresh();
  }
  
  onAppEventLogout(evt, data) {
    this.refresh();
  }
  //#endregion

  //#region UI EVENTS
  onSubmitClick() {
    if(this.state.mode == mode.NEW) {
      ServerApi.createBook(this.state.data)
      .then(json => {
        GlobalState.raiseEvent(Events.NOTIFICATION, "Successfully added a new book!");
        window.location.hash = `#/edit/${json.id}`;
        return json;
      })
      .catch(err => console.error(err));
    } 
    else if(this.state.mode == mode.EDIT) {
      ServerApi.editBook(this.state.data)
      .then(json => {
        GlobalState.raiseEvent(Events.NOTIFICATION, "Editing was successful!");
        return json;
      })
      .catch(err => console.error(err));
    }
  }

  onValueChange(event) {
    let newState = { ...this.state };
    newState.data[event.srcElement.id] = event.srcElement.value;

    this.setState(newState);
  }

  bindChangeToEvent(name) {
    return (event) => { this.onValueChange(name, event); };
  }

  onCancelClick() {
    window.location.hash = '#/';
  }

  onCategoryClick(id) {
    if(this.state.data.categories.find(x => x == id))
      this.state.data.categories = this.state.data.categories.filter(x => x != id);
    else
      this.state.data.categories.push(id);
    this.setState({...this.state});
  }

  bindCategoryClick(id) {
    return () => this.onCategoryClick(id);
  }

  getButtonStyle(id) {
    if(this.state.data.categories.find(x => x == id))
      return styles.clicked;
    return styles.unclicked;
  }
  //#endregion

  //#region INTERNAL FUNCTIONS
  initialState() {
    const { match: { params } } = this.props;
    let id = params != null && params.id != null 
      ? params.id 
      : null;

    // we need these lines to get access to the route id
    return {
      name: '',
      data: {
        id: id,
        categories: []
      },
      categories: this.state ? this.state.categories : [],
      loggedIn: GlobalState.getStateData(State.CURRENT_USER) != null,
      mode: id != null ? mode.EDIT : mode.NEW
    };
  }

  refresh() {
    if(this.state.categories == null || this.state.categories.length == 0) {
      // Because of the async nature of retrieving the categories,
      // we need to retrieve the categories and queue the rest of the refresh
      categories.then(json => {
        this.setState({
          ...this.state,
          categories: json
        }, 
        this.refresh)
        return;
      });
    }

    const { match: { params } } = this.props;
    let id = params != null && params.id != null 
      ? params.id 
      : null;

    let newState = this.initialState();
    newState.loggedIn = GlobalState.getStateData(State.CURRENT_USER) != null;
    newState.data.id = id;
    newState.mode = id == null ? mode.NEW : mode.EDIT;
    newState.categories = this.state.categories;

    if(newState.data.id && newState.loggedIn) {
      ServerApi
        .fetchBook(newState.data.id)
        .then(json => {
          newState.data = json;
          newState.data.categories = json.categories.map((value, index) => value.id);
          newState.name = json.name;
          this.setState(newState);
          return json;
        })
        .catch(err => console.error(err));
    } else {
      this.setState(newState);
    }
  }
  //#endregion
  
  render() {
    if(this.state.loggedIn == false) {
      return <div><p>Please login to edit your books.</p></div>
    }
    let title = this.state.mode == mode.NEW
      ? `You're adding a new book!`
      : `You're editing ${this.state.name}!`

    return (
      <div className={styles.root}>
        <h2>{title}</h2>

        <div className={styles.row}>
          <div className={styles.labelColumn}>
            <label for="name">Name:</label>
          </div>
          <div className={styles.inputColumn}>
            <input id="name" name="name" type="text" onInput={this.onValueChange} value={this.state.data.name} />
          </div>
        </div>

        <div className={styles.row}>
          <div className={styles.labelColumn}>
            <label for="description">Description:</label>
          </div>
          <div className={styles.inputColumn}>
            <input id="description" name="description" type="text" onInput={this.onValueChange} value={this.state.data.description} />
          </div>
        </div>

        <div className={styles.row}>
          <div className={styles.labelColumn}>
            <label for="web_link">Web link:</label>
          </div>
          <div className={styles.inputColumn}>
            <input id="web_link" name="web_link" type="text" onInput={this.onValueChange} value={this.state.data.web_link} />
          </div>
        </div>

        <div className={styles.row}>
          <div className={styles.labelColumn}>
            <label for="author">Author:</label>
          </div>
          <div className={styles.inputColumn}>
            <input id="author" name="author" type="text" onInput={this.onValueChange} value={this.state.data.author} />
          </div>
        </div>

        <div className={styles.row}>
          <div className={styles.labelColumn}>
            <label for="publisher">Publisher:</label>
          </div>
          <div className={styles.inputColumn}>
            <input id="publisher" name="publisher" type="text" onInput={this.onValueChange} value={this.state.data.publisher} />
          </div>
        </div>

        <div className={styles.row}>
          <div className={styles.labelColumn}>
            <span>Categories:</span>
          </div>
          <div className={styles.inputColumn}>
            <div className={styles.row}>
            {
              this.state.categories.map((val, index) => (
                <div className={styles.categoryColumn}>
                  <button className={this.getButtonStyle(val.id)} onClick={this.bindCategoryClick(val.id)}>{ val.name }</button>
                </div>
              ))
            }
            </div>
          </div>
        </div>

        <div className={styles.row}>
          <div className={styles.labelColumn}>
          </div>
          <div className={styles.buttonColumn}>
            <button onClick={linkEvent(this, this.onCancelClick)}>Cancel</button>
          </div>
          <div className={styles.buttonColumn}>
            <button onClick={linkEvent(this, this.onSubmitClick)}>Submit</button>
          </div>
        </div>
      </div>
    );
  }
}