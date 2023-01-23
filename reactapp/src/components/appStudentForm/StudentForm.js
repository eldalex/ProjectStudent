import {useEffect, useState} from "react";
import {Button, Form, FormGroup, Input, Label} from "reactstrap";
import axios from "axios";
import {API_URL} from "../../index";

const StudentForm = (props) => {
    const [student, setStudent] = useState({})

    const onChange = (e) => {
        const newState = student
        if (e.target.name === "file") {
            newState[e.target.name] = e.target.files[0]
        } else newState[e.target.name] = e.target.value
        setStudent(newState)
    }

    useEffect(() => {
        if (!props.newStudent) {
            setStudent(student => props.student)
        }
        // eslint-disable-next-line
    }, [props.student])


    const defaultIfEmpty = value => {
        return value === "" ? "" : value;
    }

    const submitDataEdit = async (e) => {
        e.preventDefault();
        // eslint-disable-next-line
        const result = await axios.put(API_URL + student.pk, student, {headers: {'Content-Type': 'multipart/form-data'}})
            .then(() => {
                props.resetState()
                props.toggle()
            })
    }
    const submitDataAdd = async (e) => {
        e.preventDefault();
        const data = {
            name: student['name'],
            email: student['email'],
            document: student['document'],
            phone: student['phone'],
            photo: "/",
            file: student['file']
        }
        // eslint-disable-next-line
        const result = await axios.post(API_URL, data, {headers: {'Content-Type': 'multipart/form-data'}})
            .then(() => {
                props.resetState()
                props.toggle()
            })
    }
    return (
        <Form onSubmit={props.newStudent ? submitDataAdd : submitDataEdit}>
            <FormGroup>
                <Label for="name">Name:</Label>
                <Input
                    type="text"
                    name="name"
                    onChange={onChange}
                    defaultValue={defaultIfEmpty(student.name)}
                />
            </FormGroup>
            <FormGroup>
                <Label for="email">Email</Label>
                <Input
                    type="email"
                    name="email"
                    onChange={onChange}
                    defaultValue={defaultIfEmpty(student.email)}
                />
            </FormGroup>
            <FormGroup>
                <Label for="document">Document:</Label>
                <Input
                    type="text"
                    name="document"
                    onChange={onChange}
                    defaultValue={defaultIfEmpty(student.document)}
                />
            </FormGroup>
            <FormGroup>
                <Label for="phone">Phone:</Label>
                <Input
                    type="text"
                    name="phone"
                    onChange={onChange}
                    defaultValue={defaultIfEmpty(student.phone)}
                />
            </FormGroup>
            <FormGroup>
                <Label for="photo">Photo:</Label>
                <Input
                    type="file"
                    name="file"
                    onChange={onChange}
                    accept='image/*'
                />
            </FormGroup>
            <div style={{display: "flex", justifyContent: "space-between"}}>
                <Button>Send</Button> <Button onClick={props.toggle}>Cancel</Button>
            </div>
        </Form>
    )
}

export default StudentForm;