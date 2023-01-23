import {Fragment, useState} from "react";
import {Button, Modal, ModalHeader, ModalFooter} from "reactstrap";
import axios from "axios";
import {API_URL} from "../../index";

const AppRemoveStudent = (props) => {
    const [visible, setVisible] = useState(false)
    const toggle = () => {
        setVisible(!visible)
    }
    const deleteStudent = () => {
        axios.delete(API_URL + props.pk).then(() => {
            props.resetState()
            toggle();
        });
    }
    return (
        <Fragment>
            <Button color="danger" onClick={() => toggle()}>
                Удалить
            </Button>
            <Modal isOpen={visible} toggle={toggle} style={{width: "300px"}}>
                <ModalHeader style={{justifyContent: "center"}}>Вы уверены?</ModalHeader>
                <ModalFooter style={{display: "flex", justifyContent: "space-between"}}>
                    <Button
                        type="button"
                        onClick={() => deleteStudent()}
                        color="primary"
                    >Удалить</Button>
                    <Button type="button" onClick={() => toggle()}>Отмена</Button>
                </ModalFooter>
            </Modal>
        </Fragment>
    )
}
export default AppRemoveStudent;