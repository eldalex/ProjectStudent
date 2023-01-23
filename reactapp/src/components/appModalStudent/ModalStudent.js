import {Fragment, useState} from "react";
import {Button, Modal, ModalHeader, ModalBody} from "reactstrap";
import StudentForm from "../appStudentForm/StudentForm";

const ModalStudent = (props) => {
    const [visible, setVisible] = useState(false)
    var button = <Button onClick={() => toggle()}>Редактировать</Button>;

    const toggle = () => {
        setVisible(!visible)
    }

    if (props.create) {
        button = (
            <Button
                color="primary"
                className="float-right"
                onClick={() => toggle()}
                style={{minWidth: "200px"}}>
                Добавить студента
            </Button>
        )
    }
    return (
        <Fragment>
            {button}
            <Modal isOpen={visible} toggle={toggle}>
                <ModalHeader
                    style={{justifyContent: "center"}}>{props.create ? "Добавить студента" : "Редактировать студента"}</ModalHeader>
                <ModalBody>
                    <StudentForm
                        student={props.student ? props.student : []}
                        resetState={props.resetState}
                        toggle={toggle}
                        newStudent={props.newStudent}
                    />
                </ModalBody>
            </Modal>
        </Fragment>
    )
}
export default ModalStudent;