import axios from "axios";

// شكل البيانات المقترح في الباك-إند:
// { id, title, date, time, place, desc }

export const getEvents = () => axios.get("events/");            // GET /api/events/
export const createEvent = (data) => axios.post("events/", data); // POST
export const updateEvent = (id, data) => axios.put(`events/${id}/`, data); // PUT
export const deleteEvent = (id) => axios.delete(`events/${id}/`);         // DELETE
