from rest_framework import permissions


class IsCreatedRoom(permissions.BasePermission):

  def has_object_permission(self, request, view, obj):

    # Read-only permissions are allowed for any request

    if request.method in permissions.SAFE_METHODS:
      return True

    # Write permissions are only allowed to the author of a message

    return obj.created_by == request.user
  


class IsCreatedMessage(permissions.BasePermission):

  def has_object_permission(self, request, view, obj):

    # Read-only permissions are allowed for any request

    if request.method in permissions.SAFE_METHODS:
      return True

    # Write permissions are only allowed to the author of a message

    return obj.person == request.user


class IsCreatedChannel(permissions.BasePermission):

  def has_object_permission(self, request, view, obj):

    # Read-only permissions are allowed for any request

    if request.method in permissions.SAFE_METHODS:
      return True

    # Write permissions are only allowed to the author of a message

    return obj.room.created_by == request.user


class IsMemberOfRoom(permissions.BasePermission):

  def has_object_permission(self, request, view, obj):

    # Read-only permissions are allowed for any request

    # if request.method in permissions.SAFE_METHODS:
    #   return True

    # Write permissions are only allowed to the author of a message

    return obj.person == request.user




    