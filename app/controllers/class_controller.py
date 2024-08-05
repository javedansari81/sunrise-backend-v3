from flask import request, jsonify
from bson import ObjectId
from flasgger import swag_from
from app.models.class_model import  ClassModel
from app.models.classDetail_model import ClassDetailModel
from app import mongo

class_model = ClassModel(mongo)
classDetail_model=ClassDetailModel(mongo)


def create_class():
    data = request.json
    class_data = {
        "className": data["className"],
        "aboutClass": data["aboutClass"],
        "students": data["students"],
        "classUrl":data['classUrl'],
        "isActive":data['isActive']
       
    }


    class_id = class_model.create(class_data)

    classDetail_data = {
        "classId":class_id,
        "className": data["className"],
        "aboutClass": data["aboutClass"],
        "subjects": data['subjects'],
        
    }
   
    classDetail_model.create(classDetail_data)
    



    return jsonify({"message": "Class and Details created successfully", "class_id": str(class_id)}), 201


def get_classes():
    classes = class_model.find({}) #find all classes
    if not classes:
        return jsonify({'message': 'No classes found'}), 404
    
    classes_data=[]
    
    for student_class in classes:
        # fetch class_detail by class_id
        class_details= classDetail_model.find_one({"classId":student_class['_id']})
        

      
        # class_data with class_details
        class_data = {
        "_id":str(student_class['_id']),
        "className": student_class["className"],
        "aboutClass": student_class["aboutClass"],
        "students": student_class["students"],
        "classUrl":student_class['classUrl'],
        "isActive":student_class['isActive']
       } 
        if class_details:
            class_data.update({
                "subjects": class_details['subjects'],


            })
        classes_data.append(class_data)
    
    return jsonify(classes_data), 200

def get_class(class_id):
    student_class= class_model.find_one({'_id': ObjectId(class_id)})
    if not student_class:
        return jsonify({'error': 'Class not found'}), 404
    
    # fetch class Detail by class_id
    class_details=classDetail_model.find_one({'classId':ObjectId(class_id)})

    if not class_details:
        return jsonify({'error':'class details not found'}),404
    

    # new class data
    class_data={
        "_id":str(student_class['_id']),
        "className": student_class["className"],
        "aboutClass": student_class["aboutClass"],
        "students": student_class["students"],
        "classUrl":student_class['classUrl'],
        "isActive":student_class['isActive'] ,
        "subjects": class_details['subjects']
    }
    
    return jsonify(class_data), 200


def update_class(class_id):
    updated_data = request.json
    updating_class= class_model.find_one({'_id': ObjectId(class_id)})
    if not updating_class:
        return jsonify({'error': 'Class not found'}), 404

    class_data = {
        "className": updated_data["className"],
        "aboutClass": updated_data["aboutClass"],
        "students": updated_data["students"],
        "classUrl":updated_data['classUrl'],
        "subjects": updated_data['subjects']

    }

    result = class_model.update({'_id': ObjectId(class_id)}, class_data)
    classDetail_model.update({'classId':ObjectId(updating_class['_id'])},class_data)
    
    
    if result.modified_count == 0:
        return jsonify({'error': 'Class update failed'}), 500
    
    return jsonify({'message': 'Class updated successfully'}), 200


def delete_class(class_id):
    
    result = class_model.delete({'_id': ObjectId(class_id)})
    if result.deleted_count == 0:
        return jsonify({'error': 'Class not found or delete failed'}), 404
    
    class_detail_data = classDetail_model.delete({'classId':ObjectId(class_id)})

   
    return jsonify({'message': 'Class and detail deleted successfully'}), 200